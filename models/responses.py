"""Pydantic response models for WSG Courses API endpoints."""

from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict
from datetime import datetime


class APIResponse(BaseModel):
    """Base API response model."""
    
    success: bool = Field(default=True, description="Request success status")
    data: Optional[Any] = Field(default=None, description="Response data")
    message: Optional[str] = Field(default=None, description="Response message")
    error: Optional[str] = Field(default=None, description="Error message if any")


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Items per page")
    total_results: Optional[int] = Field(default=None, description="Total number of results")
    has_more: Optional[bool] = Field(default=None, description="Whether more pages exist")


class Category(BaseModel):
    """Course category model."""
    
    id: Optional[int] = None
    name: Optional[str] = None
    display: Optional[bool] = None


class Tag(BaseModel):
    """Course tag model."""
    
    text: Optional[str] = None
    count: Optional[int] = None


class CourseProvider(BaseModel):
    """Training provider model."""
    
    name: Optional[str] = None
    uen: Optional[str] = None
    code: Optional[str] = None


class CourseRun(BaseModel):
    """Course run/schedule model."""
    
    run_id: Optional[str] = Field(default=None, alias="runId")
    start_date: Optional[str] = Field(default=None, alias="startDate")
    end_date: Optional[str] = Field(default=None, alias="endDate")
    venue: Optional[str] = None
    vacancy: Optional[str] = None
    schedule: Optional[str] = None
    
    model_config = {"populate_by_name": True}


class Course(BaseModel):
    """Course details model."""
    
    ref_number: Optional[str] = Field(default=None, alias="referenceNumber")
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = Field(default=None, alias="subCategory")
    provider: Optional[CourseProvider] = None
    course_fee: Optional[float] = Field(default=None, alias="courseFee")
    duration: Optional[str] = None
    duration_hours: Optional[float] = Field(default=None, alias="durationHours")
    training_mode: Optional[str] = Field(default=None, alias="trainingMode")
    tags: Optional[List[Tag]] = None
    runs: Optional[List[CourseRun]] = None
    url: Optional[str] = None
    
    model_config = {"populate_by_name": True}


class CategoryResponse(APIResponse):
    """Response model for category endpoints."""
    
    data: Optional[List[Category]] = None


class TagResponse(APIResponse):
    """Response model for tag endpoints."""
    
    data: Optional[List[Tag]] = None


class CourseSearchResponse(APIResponse):
    """Response model for course search endpoints."""
    
    data: Optional[List[Course]] = None
    meta: Optional[PaginationMeta] = None


class CourseDetailResponse(APIResponse):
    """Response model for course detail endpoint."""
    
    data: Optional[Course] = None


class AutocompleteResponse(APIResponse):
    """Response model for autocomplete endpoint."""
    
    data: Optional[Dict[str, Any]] = None


class SubCategoryResponse(APIResponse):
    """Response model for subcategory endpoint."""
    
    data: Optional[List[Category]] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    detail: Optional[str] = Field(default=None, description="Additional error details")
    timestamp: str = Field(description="Error timestamp")
