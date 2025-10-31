"""FastAPI router for WSG Courses API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from typing import Annotated, Optional
import httpx
import logging
from datetime import datetime

from dependencies.auth import get_cert_client
from models.responses import (
    CategoryResponse, TagResponse, CourseSearchResponse,
    CourseDetailResponse, AutocompleteResponse, SubCategoryResponse,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error"},
        503: {"model": ErrorResponse, "description": "Service unavailable"}
    }
)


@router.get(
    "/categories",
    response_model=CategoryResponse,
    summary="Get course categories",
    description="Retrieve course categories by keyword (API v1)"
)
async def get_categories(
    keyword: Annotated[str, Query(min_length=1, description="Search keyword for categories")] = "training",
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get course categories by keyword."""
    try:
        response = await client.get(
            f"/courses/categories",
            params={"keyword": keyword}
        )
        response.raise_for_status()
        
        api_response = response.json()
        categories_data = api_response.get("data", {}).get("categories", [])
        logger.info(f"Retrieved {len(categories_data)} categories")
        
        return CategoryResponse(
            success=True,
            data=categories_data
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting categories: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting categories: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve categories: {str(e)}"
        )


@router.get(
    "/tags",
    response_model=TagResponse,
    summary="Get course tags",
    description="Retrieve all available course tags (API v1)"
)
async def get_tags(
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get all course tags."""
    try:
        response = await client.get("/courses/tags")
        response.raise_for_status()
        
        api_response = response.json()
        return TagResponse(
            success=True,
            data=api_response.get("data", {}).get("tags", [])
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting tags: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting tags: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tags"
        )


@router.get(
    "/directory",
    response_model=CourseSearchResponse,
    summary="Search courses by keyword",
    description="Search courses by keyword with pagination (API v2.2)"
)
async def search_courses(
    keyword: Annotated[str, Query(min_length=3, description="Search keyword")] = "python",
    page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 10,
    page: Annotated[int, Query(ge=0, description="Page number (0-indexed)")] = 0,
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Search courses by keyword."""
    try:
        response = await client.get(
            "/courses/directory",
            params={
                "keyword": keyword,
                "pageSize": page_size,
                "page": page
            }
        )
        response.raise_for_status()
        
        api_response = response.json()
        course_data = api_response.get("data", {})
        courses = course_data.get("courses", [])
        total = course_data.get("totalResults")
        
        logger.info(f"Retrieved {len(courses)} courses (total: {total})")
        
        return CourseSearchResponse(
            success=True,
            data=courses,
            meta={
                "page": page,
                "page_size": page_size,
                "total_results": total
            }
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error searching courses: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error searching courses: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search courses: {str(e)}"
        )


@router.post(
    "/directory/search-by-tagging",
    response_model=CourseSearchResponse,
    summary="Search courses by tagging codes",
    description="Search courses by tagging codes (API v2.2)"
)
async def search_by_tagging(
    tagging_codes: Annotated[list[str], Query(description="Tagging codes or ['FULL']")],
    support_end_date: Annotated[str, Query(pattern=r"^\d{8}$", description="YYYYMMDD format")],
    retrieve_type: Annotated[str, Query(pattern="^(FULL|DELTA)$")] = "FULL",
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    page: Annotated[int, Query(ge=0)] = 0,
    last_update_date: Annotated[Optional[str], Query(pattern=r"^\d{8}$")] = None,
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Search courses by tagging codes."""
    try:
        # Validate last_update_date for DELTA
        if retrieve_type == "DELTA" and not last_update_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="last_update_date is required when retrieve_type is DELTA"
            )
        
        params = {
            "taggingCode": ",".join(tagging_codes),
            "supportEndDate": support_end_date,
            "retrieveType": retrieve_type,
            "pageSize": page_size,
            "page": page
        }
        
        if last_update_date:
            params["lastUpdateDate"] = last_update_date
        
        response = await client.get("/courses/directory", params=params)
        response.raise_for_status()
        
        api_response = response.json()
        course_data = api_response.get("data", {})
        
        return CourseSearchResponse(
            success=True,
            data=course_data.get("courses", []),
            meta={
                "page": page,
                "page_size": page_size,
                "total_results": course_data.get("totalResults")
            }
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error searching by tagging: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error searching by tagging: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search courses by tagging"
        )


@router.get(
    "/directory/autocomplete",
    response_model=AutocompleteResponse,
    summary="Get autocomplete suggestions",
    description="Get course title autocomplete suggestions (API v1.2)"
)
async def get_autocomplete(
    keyword: Annotated[str, Query(min_length=1, description="Search keyword")] = "python",
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get autocomplete suggestions for course search."""
    try:
        response = await client.get(
            "/courses/directory/autocomplete",
            params={"keyword": keyword}
        )
        response.raise_for_status()
        
        api_response = response.json()
        return AutocompleteResponse(
            success=True,
            data=api_response.get("data", {})
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting autocomplete: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting autocomplete: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get autocomplete suggestions"
        )


@router.get(
    "/categories/{category_id}/subCategories",
    response_model=SubCategoryResponse,
    summary="Get course subcategories",
    description="Get subcategories for a specific category (API v1)"
)
async def get_subcategories(
    category_id: Annotated[str, Path(description="Category ID")],
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get subcategories for a category."""
    try:
        response = await client.get(
            f"/courses/categories/{category_id}/subCategories"
        )
        response.raise_for_status()
        
        api_response = response.json()
        return SubCategoryResponse(
            success=True,
            data=api_response.get("data", {}).get("subCategories", [])
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting subcategories: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting subcategories: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve subcategories"
        )


@router.get(
    "/directory/{ref_number}",
    response_model=CourseDetailResponse,
    summary="Get course details",
    description="Get detailed information for a specific course (API v1.2)"
)
async def get_course_details(
    ref_number: Annotated[str, Path(description="Course reference number")],
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get detailed course information."""
    try:
        response = await client.get(f"/courses/directory/{ref_number}")
        response.raise_for_status()
        
        api_response = response.json()
        return CourseDetailResponse(
            success=True,
            data=api_response.get("data", {})
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting course details: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting course details: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve course details"
        )


@router.get(
    "/directory/{ref_number}/related",
    response_model=CourseSearchResponse,
    summary="Get related courses",
    description="Get courses related to a specific course (API v1)"
)
async def get_related_courses(
    ref_number: Annotated[str, Path(description="Course reference number")],
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    page: Annotated[int, Query(ge=0)] = 0,
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get related courses."""
    try:
        response = await client.get(
            f"/courses/directory/{ref_number}/related",
            params={
                "pageSize": page_size,
                "page": page
            }
        )
        response.raise_for_status()
        
        api_response = response.json()
        course_data = api_response.get("data", {})
        
        return CourseSearchResponse(
            success=True,
            data=course_data.get("courses", []),
            meta={
                "page": page,
                "page_size": page_size
            }
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting related courses: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting related courses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve related courses"
        )


@router.get(
    "/directory/popular",
    response_model=CourseSearchResponse,
    summary="Get popular courses",
    description="Get popular courses (API v1.2)"
)
async def get_popular_courses(
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    page: Annotated[int, Query(ge=0)] = 0,
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get popular courses."""
    try:
        response = await client.get(
            "/courses/directory/popular",
            params={
                "pageSize": page_size,
                "page": page
            }
        )
        response.raise_for_status()
        
        api_response = response.json()
        course_data = api_response.get("data", {})
        
        return CourseSearchResponse(
            success=True,
            data=course_data.get("courses", []),
            meta={
                "page": page,
                "page_size": page_size
            }
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting popular courses: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting popular courses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve popular courses"
        )


@router.get(
    "/directory/featured",
    response_model=CourseSearchResponse,
    summary="Get featured courses",
    description="Get featured courses (API v1.2)"
)
async def get_featured_courses(
    page_size: Annotated[int, Query(ge=1, le=100)] = 10,
    page: Annotated[int, Query(ge=0)] = 0,
    client: httpx.AsyncClient = Depends(get_cert_client)
):
    """Get featured courses."""
    try:
        response = await client.get(
            "/courses/directory/featured",
            params={
                "pageSize": page_size,
                "page": page
            }
        )
        response.raise_for_status()
        
        api_response = response.json()
        course_data = api_response.get("data", {})
        
        return CourseSearchResponse(
            success=True,
            data=course_data.get("courses", []),
            meta={
                "page": page,
                "page_size": page_size
            }
        )
        
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error getting featured courses: {e}")
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"WSG API error: {e.response.text}"
        )
    except Exception as e:
        logger.error(f"Error getting featured courses: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve featured courses"
        )
