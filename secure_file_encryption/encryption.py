from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import os

def generate_key(username: str, salt: bytes) -> bytes:
    """Generates a 256-bit AES key using username and salt."""
    return PBKDF2(username, salt, dkLen=32, count=100000)

def encrypt_file(input_file: str, output_file: str, username: str):
    """Encrypts any file using AES-GCM."""
    salt = get_random_bytes(16)
    key = generate_key(username, salt)
    cipher = AES.new(key, AES.MODE_GCM)
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    
    with open(output_file, 'wb') as f:
        f.write(salt + cipher.nonce + tag + ciphertext)

def decrypt_file(input_file: str, output_file: str, username: str):
    """Decrypts an AES-GCM encrypted file."""
    with open(input_file, 'rb') as f:
        data = f.read()

    salt, nonce, tag, ciphertext = data[:16], data[16:32], data[32:48], data[48:]
    key = generate_key(username, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)

    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        with open(output_file, 'wb') as f:
            f.write(plaintext)
        return True
    except ValueError:
        return False
