"""API dependencies for dependency injection"""

from typing import Optional
from fastapi import Header, HTTPException

# Example dependency for API key validation
async def get_api_key(x_api_key: Optional[str] = Header(None)) -> Optional[str]:
    """
    Validate API key from header (optional)
    
    Uncomment and modify when you need API key authentication
    """
    # if not x_api_key:
    #     raise HTTPException(status_code=401, detail="API key required")
    # if x_api_key != "your-secret-key":
    #     raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key


# Example dependency for database session
# from app.db import get_db
# def get_db_session():
#     """Get database session"""
#     return get_db()


