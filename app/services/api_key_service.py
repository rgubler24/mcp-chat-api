"""API Key service for managing encrypted API keys"""

from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.api_key import APIKey
from app.schemas.api_key import APIKeyCreate, APIKeyUpdate
from app.utils.encryption import encryption_service


class APIKeyService:
    """Service for managing API keys"""
    
    def mask_key(self, key: str) -> str:
        """
        Mask an API key for display purposes
        Shows first 8 and last 4 characters
        """
        if len(key) <= 12:
            return f"{key[:4]}...{key[-2:]}"
        return f"{key[:8]}...{key[-4:]}"
    
    def create_or_update_key(self, db: Session, key_data: APIKeyCreate) -> APIKey:
        """
        Create a new API key or update existing one
        
        Args:
            db: Database session
            key_data: API key data to create/update
            
        Returns:
            Created or updated APIKey model
        """
        # Check if key already exists
        existing_key = db.query(APIKey).filter(APIKey.name == key_data.name).first()
        
        # Encrypt the key
        encrypted_key = encryption_service.encrypt(key_data.key)
        
        if existing_key:
            # Update existing key
            existing_key.encrypted_key = encrypted_key
            existing_key.is_active = True
            db.commit()
            db.refresh(existing_key)
            return existing_key
        else:
            # Create new key
            db_key = APIKey(
                name=key_data.name,
                encrypted_key=encrypted_key,
                is_active=True
            )
            db.add(db_key)
            db.commit()
            db.refresh(db_key)
            return db_key
    
    def get_key(self, db: Session, name: str) -> Optional[APIKey]:
        """
        Get an API key by name
        
        Args:
            db: Database session
            name: Name of the API key
            
        Returns:
            APIKey model or None
        """
        return db.query(APIKey).filter(APIKey.name == name).first()
    
    def get_decrypted_key(self, db: Session, name: str) -> Optional[str]:
        """
        Get the decrypted API key value
        
        Args:
            db: Database session
            name: Name of the API key
            
        Returns:
            Decrypted key string or None
        """
        api_key = self.get_key(db, name)
        if api_key and api_key.is_active:
            return encryption_service.decrypt(api_key.encrypted_key)
        return None
    
    def list_keys(self, db: Session) -> List[APIKey]:
        """
        List all API keys
        
        Args:
            db: Database session
            
        Returns:
            List of APIKey models
        """
        return db.query(APIKey).all()
    
    def delete_key(self, db: Session, name: str) -> bool:
        """
        Delete an API key
        
        Args:
            db: Database session
            name: Name of the API key
            
        Returns:
            True if deleted, False if not found
        """
        api_key = self.get_key(db, name)
        if api_key:
            db.delete(api_key)
            db.commit()
            return True
        return False
    
    def update_key_status(self, db: Session, name: str, is_active: bool) -> Optional[APIKey]:
        """
        Update API key active status
        
        Args:
            db: Database session
            name: Name of the API key
            is_active: New active status
            
        Returns:
            Updated APIKey model or None
        """
        api_key = self.get_key(db, name)
        if api_key:
            api_key.is_active = is_active
            db.commit()
            db.refresh(api_key)
            return api_key
        return None


# Singleton instance
api_key_service = APIKeyService()

