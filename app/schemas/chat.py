"""Chat-related Pydantic schemas"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message role enumeration"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    """Chat message schema"""
    id: Optional[str] = None
    role: MessageRole
    content: str
    timestamp: Optional[datetime] = None
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "user",
                "content": "Hello, how can you help me?",
                "timestamp": "2025-11-04T10:00:00Z"
            }
        }


class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., min_length=1, description="User message")
    session_id: Optional[str] = Field(None, description="Session ID for conversation continuity")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context for the message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is FastAPI?",
                "session_id": "session-123",
                "context": {"user_id": "user-456"}
            }
        }


class ChatResponse(BaseModel):
    """Chat response schema"""
    message: str = Field(..., description="Assistant response")
    session_id: str = Field(..., description="Session ID")
    message_id: Optional[str] = Field(None, description="Unique message ID")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "FastAPI is a modern web framework for building APIs with Python.",
                "session_id": "session-123",
                "message_id": "msg-789",
                "timestamp": "2025-11-04T10:00:01Z"
            }
        }


class ChatSessionCreate(BaseModel):
    """Schema for creating a new chat session"""
    title: Optional[str] = Field(None, description="Session title")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional session metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "My Chat Session",
                "metadata": {"user_id": "user-456"}
            }
        }


class ChatSession(BaseModel):
    """Chat session schema"""
    id: str = Field(..., description="Unique session ID")
    title: Optional[str] = Field(None, description="Session title")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    message_count: int = Field(0, description="Number of messages in session")
    metadata: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "session-123",
                "title": "My Chat Session",
                "created_at": "2025-11-04T10:00:00Z",
                "updated_at": "2025-11-04T10:05:00Z",
                "message_count": 5
            }
        }


