"""Encryption utilities for API keys"""

from cryptography.fernet import Fernet
import base64
import os
from app.core.config import settings


class EncryptionService:
    """Service for encrypting and decrypting API keys"""
    
    def __init__(self):
        # Get encryption key from environment or generate one
        # In production, store this in a secure environment variable
        encryption_key = os.getenv("ENCRYPTION_KEY")
        
        if not encryption_key:
            # Generate a key for development (WARNING: not for production!)
            # In production, set ENCRYPTION_KEY environment variable
            encryption_key = Fernet.generate_key().decode()
            print(f"⚠️  Generated encryption key (for development only): {encryption_key}")
            print("⚠️  Set ENCRYPTION_KEY environment variable in production!")
        
        if isinstance(encryption_key, str):
            encryption_key = encryption_key.encode()
            
        self.cipher = Fernet(encryption_key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt a plaintext string
        
        Args:
            plaintext: The string to encrypt
            
        Returns:
            Encrypted string (base64 encoded)
        """
        encrypted_bytes = self.cipher.encrypt(plaintext.encode())
        return encrypted_bytes.decode()
    
    def decrypt(self, encrypted_text: str) -> str:
        """
        Decrypt an encrypted string
        
        Args:
            encrypted_text: The encrypted string to decrypt
            
        Returns:
            Decrypted plaintext string
        """
        decrypted_bytes = self.cipher.decrypt(encrypted_text.encode())
        return decrypted_bytes.decode()


# Singleton instance
encryption_service = EncryptionService()

