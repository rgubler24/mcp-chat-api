"""API Key Pydantic schemas"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class APIKeyCreate(BaseModel):
    """Schema for creating/updating an API key"""
    name: str = Field(..., description="Name of the API key (e.g., 'openai', 'anthropic')")
    key: str = Field(..., min_length=1, description="The actual API key value")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "openai",
                "key": "sk-proj-..."
            }
        }


class APIKeyResponse(BaseModel):
    """Schema for API key response (without the actual key)"""
    id: int
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    masked_key: str = Field(..., description="Partially masked API key for verification")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "openai",
                "is_active": True,
                "created_at": "2025-11-04T10:00:00Z",
                "updated_at": "2025-11-04T10:00:00Z",
                "masked_key": "sk-proj-...xyz"
            }
        }


class APIKeyUpdate(BaseModel):
    """Schema for updating an API key"""
    key: Optional[str] = Field(None, min_length=1, description="New API key value")
    is_active: Optional[bool] = Field(None, description="Whether the key is active")
    
    class Config:
        json_schema_extra = {
            "example": {
                "key": "sk-proj-...",
                "is_active": True
            }
        }


class APIKeyList(BaseModel):
    """Schema for listing API keys"""
    keys: list[APIKeyResponse]
    total: int

