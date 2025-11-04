"""API Key database model"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.db import Base


class APIKey(Base):
    """Model for storing API keys"""
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True, nullable=False)  # e.g., "openai", "anthropic"
    encrypted_key = Column(String, nullable=False)  # Encrypted API key
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<APIKey(name='{self.name}', is_active={self.is_active})>"

