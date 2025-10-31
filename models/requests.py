"""Pydantic request models for WSG Courses API endpoints."""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import datetime


class CourseSearchRequest(BaseModel):
    """Request model for course search by keyword."""
    
    keyword: str = Field(
        ...,
        min_length=3,
        description="Search keyword (minimum 3 characters)",
        examples=["python programming"]
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page"
    )
    page: int = Field(
        default=0,
        ge=0,
        description="Page number, starting from 0"
    )


class CourseTaggingRequest(BaseModel):
    """Request model for course search by tagging codes."""
    
    tagging_codes: List[str] = Field(
        ...,
        description="List of tagging codes or ['FULL'] for all courses",
        examples=[["1", "2"], ["FULL"]]
    )
    support_end_date: str = Field(
        ...,
        pattern=r"^\d{8}$",
        description="Format YYYYMMDD (e.g., 20250101)",
        examples=["20250101"]
    )
    retrieve_type: str = Field(
        default="FULL",
        pattern="^(FULL|DELTA)$",
        description="FULL for all courses, DELTA for changed courses"
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of items per page"
    )
    page: int = Field(
        default=0,
        ge=0,
        description="Page number, starting from 0"
    )
    last_update_date: Optional[str] = Field(
        default=None,
        pattern=r"^\d{8}$",
        description="Required if retrieve_type=DELTA. Format YYYYMMDD"
    )
    
    @field_validator('last_update_date')
    @classmethod
    def validate_last_update_date(cls, v, info):
        """Validate last_update_date is provided when retrieve_type is DELTA."""
        if info.data.get('retrieve_type') == 'DELTA' and not v:
            raise ValueError('last_update_date is required when retrieve_type is DELTA')
        return v
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "tagging_codes": ["1", "2"],
                "support_end_date": "20250101",
                "retrieve_type": "FULL",
                "page_size": 10,
                "page": 0
            }
        }
    }


class CategorySearchRequest(BaseModel):
    """Request model for category search."""
    
    keyword: str = Field(
        ...,
        min_length=1,
        description="Search keyword for categories",
        examples=["training"]
    )


class AutocompleteRequest(BaseModel):
    """Request model for course autocomplete."""
    
    keyword: str = Field(
        ...,
        min_length=1,
        description="Search keyword for autocomplete",
        examples=["python"]
    )


class PopularCoursesRequest(BaseModel):
    """Request model for popular courses."""
    
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of popular courses to retrieve"
    )
    page: int = Field(
        default=0,
        ge=0,
        description="Page number, starting from 0"
    )


class FeaturedCoursesRequest(BaseModel):
    """Request model for featured courses."""
    
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of featured courses to retrieve"
    )
    page: int = Field(
        default=0,
        ge=0,
        description="Page number, starting from 0"
    )


class RelatedCoursesRequest(BaseModel):
    """Request model for related courses."""
    
    ref_number: str = Field(
        ...,
        description="Course reference number",
        examples=["TGS-2020500330"]
    )
    page_size: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of related courses to retrieve"
    )
    page: int = Field(
        default=0,
        ge=0,
        description="Page number, starting from 0"
    )
