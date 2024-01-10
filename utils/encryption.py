from error_logging import log_error
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_ENCRIPTION_KEY = os.getenv("SECRET_ENCRIPTION_KEY") # should be of 32 bytes

def encrypt_private_key(private_key: str, key: str) -> str:
    try:
        key = key.encode('utf-8') # Convert the key to bytes
        iv = get_random_bytes(16)  # Generate a random 16-byte IV
        cipher = AES.new(key, AES.MODE_CBC, iv) # Create an AES cipher object with the key using the mode CBC
        padded_private_key = pad(private_key.encode('utf-8'), AES.block_size) # Pad the private_key so that its length is a multiple of 16
        ciphertext = cipher.encrypt(padded_private_key) # Encrypt the private_key
        encrypted_private_key = iv + ciphertext
        return encrypted_private_key
    except Exception as e:
        log_error(e, function=encrypt_private_key.__name__)
        return None

def decrypt_private_key(encrypted_private_key: str, key: str) -> str:
    try:
        key = key.encode('utf-8') # Convert the key to bytes
        iv = encrypted_private_key[:16] # Extract the IV from the beginning of the ciphertext
        cipher = AES.new(key, AES.MODE_CBC, iv) # Create an AES cipher object with the key using the mode CBC
        decrypted_private_key = unpad(cipher.decrypt(encrypted_private_key[16:]), AES.block_size) # Decrypt the ciphertext and then up-pad the result
        return decrypted_private_key.decode('utf-8')
    except Exception as e:
        log_error(e, function=decrypt_private_key.__name__)
        return None

