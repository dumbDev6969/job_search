import bcrypt
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Password Hashing Functions (one-way encryption)

def hash_password(password):
    """
    Hash a password using bcrypt (one-way encryption).
    
    Args:
        password (str): The plain text password to hash
        
    Returns:
        bytes: The hashed password
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    
    return hashed_password


def verify_password(plain_password, hashed_password):
    """
    Verify a password against a hashed password.
    
    Args:
        plain_password (str): The plain text password to verify
        hashed_password (bytes): The hashed password to check against
        
    Returns:
        bool: True if the password matches, False otherwise
    """
    if isinstance(plain_password, str):
        plain_password = plain_password.encode('utf-8')
    
    return bcrypt.checkpw(plain_password, hashed_password)


# Symmetric Encryption Functions (two-way encryption)

def generate_key(password, salt=None):
    """
    Generate a key for symmetric encryption based on a password.
    
    Args:
        password (str): The password to derive the key from
        salt (bytes, optional): A salt for key derivation. If None, a new one is generated.
        
    Returns:
        tuple: (key, salt) where key is the encryption key and salt is the salt used
    """
    if isinstance(password, str):
        password = password.encode('utf-8')
    
    if salt is None:
        salt = os.urandom(16)
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key, salt


def encrypt_data(data, password):
    """
    Encrypt data using a password (two-way encryption).
    
    Args:
        data (str or bytes): The data to encrypt
        password (str): The password to encrypt with
        
    Returns:
        dict: A dictionary containing the encrypted data and the salt used
              {'encrypted': encrypted_data, 'salt': salt}
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Generate a key from the password
    key, salt = generate_key(password)
    
    # Create a Fernet cipher with the key
    cipher = Fernet(key)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(data)
    
    return {
        'encrypted': encrypted_data,
        'salt': salt
    }


def decrypt_data(encrypted_data, password, salt):
    """
    Decrypt data using a password and the salt used during encryption.
    
    Args:
        encrypted_data (bytes): The encrypted data
        password (str): The password used for encryption
        salt (bytes): The salt used during encryption
        
    Returns:
        bytes: The decrypted data
    """
    # Generate the same key using the password and salt
    key, _ = generate_key(password, salt)
    
    # Create a Fernet cipher with the key
    cipher = Fernet(key)
    
    # Decrypt the data
    decrypted_data = cipher.decrypt(encrypted_data)
    
    return decrypted_data