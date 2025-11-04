"""Chat endpoints"""

from fastapi import APIRouter, HTTPException
from typing import List

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
    ChatSession,
    ChatSessionCreate
)
from app.services.chat_service import chat_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def send_message(request: ChatRequest):
    """
    Send a chat message and get a response
    """
    try:
        response = await chat_service.process_message(
            message=request.message,
            session_id=request.session_id,
            context=request.context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sessions", response_model=ChatSession)
async def create_session(session: ChatSessionCreate):
    """
    Create a new chat session
    """
    try:
        new_session = await chat_service.create_session(
            title=session.title,
            metadata=session.metadata
        )
        return new_session
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}", response_model=ChatSession)
async def get_session(session_id: str):
    """
    Get a chat session by ID
    """
    session = await chat_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@router.get("/sessions", response_model=List[ChatSession])
async def list_sessions(limit: int = 10, offset: int = 0):
    """
    List all chat sessions
    """
    try:
        sessions = await chat_service.list_sessions(limit=limit, offset=offset)
        return sessions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a chat session
    """
    success = await chat_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"message": "Session deleted successfully"}


@router.get("/sessions/{session_id}/messages", response_model=List[ChatMessage])
async def get_session_messages(session_id: str):
    """
    Get all messages from a chat session
    """
    try:
        messages = await chat_service.get_session_messages(session_id)
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


