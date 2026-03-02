from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import base64
import hashlib

class AESCipher:
    def __init__(self, key):
        """Initialize with a pre-shared key"""
        # Derive a 32-byte key using SHA-256
        self.key = hashlib.sha256(key.encode()).digest()
        print(f"🔑 Encryption initialized with key hash: {hashlib.sha256(key.encode()).hexdigest()[:16]}...")
    
    def encrypt(self, data):
        """Encrypt data using AES-CBC mode"""
        try:
            # Generate a random IV (Initialization Vector)
            iv = os.urandom(16)
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Convert data to bytes if it's string
            if isinstance(data, str):
                data = data.encode('utf-8')
            
            # Pad and encrypt data
            padded_data = pad(data, AES.block_size)
            encrypted = cipher.encrypt(padded_data)
            
            # Combine IV and encrypted data, then base64 encode
            combined = iv + encrypted
            return base64.b64encode(combined).decode('utf-8')
        except Exception as e:
            print(f"Encryption error: {e}")
            return None
    
    def decrypt(self, encrypted_data):
        """Decrypt data using AES-CBC mode"""
        try:
            # Decode from base64
            combined = base64.b64decode(encrypted_data)
            
            # Extract IV (first 16 bytes)
            iv = combined[:16]
            encrypted = combined[16:]
            
            # Create cipher
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            
            # Decrypt and unpad
            decrypted = cipher.decrypt(encrypted)
            unpadded = unpad(decrypted, AES.block_size)
            
            return unpadded.decode('utf-8')
        except Exception as e:
            return f"[Decryption failed: {str(e)}]"

# For demonstrating key exchange concepts
class KeyExchange:
    @staticmethod
    def generate_key():
        """Generate a random key for sharing"""
        return base64.b64encode(os.urandom(32)).decode()
    
    @staticmethod
    def hash_key(key):
        """Hash a key for storage/verification"""
        return hashlib.sha256(key.encode()).hexdigest()
    
    @staticmethod
    def simulate_key_exchange():
        """Simulate a secure key exchange process"""
        print("\n🔐 SIMULATING SECURE KEY EXCHANGE")
        print("-" * 40)
        
        # Server generates a key
        server_key = KeyExchange.generate_key()
        print(f"1. Server generates random key: {server_key[:20]}...")
        print(f"   Key hash: {KeyExchange.hash_key(server_key)[:16]}...")
        
        # In real world, this would be encrypted with client's public key
        print("2. Encrypting key with client's public key...")
        print("3. Sending encrypted key to client...")
        
        # Client decrypts and verifies
        client_key = server_key  # In real implementation, client would decrypt
        print(f"4. Client receives and decrypts key")
        print(f"5. Client verifies key hash: {KeyExchange.hash_key(client_key)[:16]}...")
        
        print("\n✅ Key exchange complete! Both sides now share a secret key.")
        print("⚠️  Note: In production, use proper asymmetric encryption for key exchange")
        print("-" * 40)
        return server_key