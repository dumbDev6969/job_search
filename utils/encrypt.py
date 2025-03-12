from encrypt import hash_password, verify_password, encrypt_data, decrypt_data

# Example usage of password hashing (one-way encryption)
def password_hashing_example():
    # Hash a password
    password = "my_secure_password123"
    hashed_password = hash_password(password)
    
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed_password}")
    
    # Verify the password
    is_valid = verify_password(password, hashed_password)
    print(f"Password verification result: {is_valid}")
    
    # Try with wrong password
    wrong_password = "wrong_password"
    is_valid = verify_password(wrong_password, hashed_password)
    print(f"Wrong password verification result: {is_valid}")


# Example usage of data encryption (two-way encryption)
def data_encryption_example():
    # Data to encrypt
    sensitive_data = "This is sensitive information that needs to be encrypted"
    password = "encryption_password"
    
    print(f"Original data: {sensitive_data}")
    
    # Encrypt the data
    encrypted_result = encrypt_data(sensitive_data, password)
    encrypted_data = encrypted_result['encrypted']
    salt = encrypted_result['salt']
    
    print(f"Encrypted data: {encrypted_data}")
    
    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, password, salt)
    
    print(f"Decrypted data: {decrypted_data.decode('utf-8')}")
    
    # Try with wrong password
    try:
        wrong_password = "wrong_password"
        decrypted_data = decrypt_data(encrypted_data, wrong_password, salt)
        print(f"Decrypted with wrong password: {decrypted_data.decode('utf-8')}")
    except Exception as e:
        print(f"Decryption with wrong password failed: {e}")


if __name__ == "__main__":
    print("\n=== Password Hashing Example (One-way Encryption) ===")
    password_hashing_example()
    
    print("\n=== Data Encryption Example (Two-way Encryption) ===")
    data_encryption_example()