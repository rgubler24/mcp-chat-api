"""Test cases for chat endpoints"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_session():
    """Test creating a new chat session"""
    response = client.post(
        "/api/v1/chat/sessions",
        json={"title": "Test Session"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["title"] == "Test Session"
    assert data["message_count"] == 0
    return data["id"]


def test_send_message():
    """Test sending a chat message"""
    # First create a session
    session_response = client.post(
        "/api/v1/chat/sessions",
        json={"title": "Test Session"}
    )
    session_id = session_response.json()["id"]
    
    # Send a message
    response = client.post(
        "/api/v1/chat/",
        json={
            "message": "Hello, world!",
            "session_id": session_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["session_id"] == session_id
    assert "message_id" in data


def test_list_sessions():
    """Test listing all sessions"""
    # Create a session first
    client.post(
        "/api/v1/chat/sessions",
        json={"title": "Test Session"}
    )
    
    response = client.get("/api/v1/chat/sessions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_get_session_messages():
    """Test getting messages from a session"""
    # Create session and send a message
    session_response = client.post(
        "/api/v1/chat/sessions",
        json={"title": "Test Session"}
    )
    session_id = session_response.json()["id"]
    
    client.post(
        "/api/v1/chat/",
        json={
            "message": "Test message",
            "session_id": session_id
        }
    )
    
    # Get messages
    response = client.get(f"/api/v1/chat/sessions/{session_id}/messages")
    assert response.status_code == 200
    messages = response.json()
    assert isinstance(messages, list)
    assert len(messages) >= 2  # User message + assistant response


def test_delete_session():
    """Test deleting a session"""
    # Create a session
    session_response = client.post(
        "/api/v1/chat/sessions",
        json={"title": "Test Session to Delete"}
    )
    session_id = session_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/api/v1/chat/sessions/{session_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    get_response = client.get(f"/api/v1/chat/sessions/{session_id}")
    assert get_response.status_code == 404


