"""API Key management endpoints"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.schemas.api_key import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyList,
    APIKeyUpdate
)
from app.services.api_key_service import api_key_service
from app.utils.encryption import encryption_service

router = APIRouter()


@router.post("/", response_model=APIKeyResponse, status_code=201)
async def create_or_update_api_key(
    key_data: APIKeyCreate,
    db: Session = Depends(get_db)
):
    """
    Create or update an API key
    
    If a key with the same name exists, it will be updated.
    The key is encrypted before storage.
    """
    try:
        db_key = api_key_service.create_or_update_key(db, key_data)
        
        # Get decrypted key for masking (only for response)
        decrypted_key = encryption_service.decrypt(db_key.encrypted_key)
        
        return APIKeyResponse(
            id=db_key.id,
            name=db_key.name,
            is_active=db_key.is_active,
            created_at=db_key.created_at,
            updated_at=db_key.updated_at,
            masked_key=api_key_service.mask_key(decrypted_key)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save API key: {str(e)}")


@router.get("/", response_model=APIKeyList)
async def list_api_keys(db: Session = Depends(get_db)):
    """
    List all API keys (with masked values)
    """
    try:
        keys = api_key_service.list_keys(db)
        
        key_responses = []
        for key in keys:
            decrypted_key = encryption_service.decrypt(key.encrypted_key)
            key_responses.append(APIKeyResponse(
                id=key.id,
                name=key.name,
                is_active=key.is_active,
                created_at=key.created_at,
                updated_at=key.updated_at,
                masked_key=api_key_service.mask_key(decrypted_key)
            ))
        
        return APIKeyList(keys=key_responses, total=len(key_responses))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list API keys: {str(e)}")


@router.get("/{name}", response_model=APIKeyResponse)
async def get_api_key(name: str, db: Session = Depends(get_db)):
    """
    Get a specific API key by name (with masked value)
    """
    api_key = api_key_service.get_key(db, name)
    if not api_key:
        raise HTTPException(status_code=404, detail=f"API key '{name}' not found")
    
    decrypted_key = encryption_service.decrypt(api_key.encrypted_key)
    
    return APIKeyResponse(
        id=api_key.id,
        name=api_key.name,
        is_active=api_key.is_active,
        created_at=api_key.created_at,
        updated_at=api_key.updated_at,
        masked_key=api_key_service.mask_key(decrypted_key)
    )


@router.delete("/{name}")
async def delete_api_key(name: str, db: Session = Depends(get_db)):
    """
    Delete an API key
    """
    success = api_key_service.delete_key(db, name)
    if not success:
        raise HTTPException(status_code=404, detail=f"API key '{name}' not found")
    
    return {"message": f"API key '{name}' deleted successfully"}


@router.patch("/{name}", response_model=APIKeyResponse)
async def update_api_key(
    name: str,
    update_data: APIKeyUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an API key (change the key value or active status)
    """
    api_key = api_key_service.get_key(db, name)
    if not api_key:
        raise HTTPException(status_code=404, detail=f"API key '{name}' not found")
    
    try:
        # Update key value if provided
        if update_data.key:
            encrypted_key = encryption_service.encrypt(update_data.key)
            api_key.encrypted_key = encrypted_key
        
        # Update active status if provided
        if update_data.is_active is not None:
            api_key.is_active = update_data.is_active
        
        db.commit()
        db.refresh(api_key)
        
        decrypted_key = encryption_service.decrypt(api_key.encrypted_key)
        
        return APIKeyResponse(
            id=api_key.id,
            name=api_key.name,
            is_active=api_key.is_active,
            created_at=api_key.created_at,
            updated_at=api_key.updated_at,
            masked_key=api_key_service.mask_key(decrypted_key)
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to update API key: {str(e)}")

