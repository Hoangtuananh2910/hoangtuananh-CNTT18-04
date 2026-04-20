from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import struct

# Độ dài mặc định của DES block là 8 bytes
BLOCK_SIZE = 8

def encrypt_data(plaintext_bytes, key, iv):
    """
    Mã hóa dữ liệu với DES-CBC và PKCS#7 padding.
    """
    cipher = DES.new(key, DES.MODE_CBC, iv)
    padded_data = pad(plaintext_bytes, BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded_data)
    return ciphertext

def decrypt_data(ciphertext, key, iv):
    """
    Giải mã dữ liệu và loại bỏ padding.
    Trả về (plaintext_bytes, error_message)
    """
    try:
        cipher = DES.new(key, DES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        plaintext = unpad(decrypted_padded, BLOCK_SIZE)
        return plaintext, None
    except ValueError:
        return None, "Padding không hợp lệ! (Có thể do sai khóa hoặc dữ liệu lỗi)"
    except Exception as e:
        return None, str(e)

def format_header(length):
    """
    Tạo header 4 byte chứa độ dài ciphertext (big-endian).
    """
    return struct.pack('>I', length)

def parse_header(header_bytes):
    """
    Đọc độ dài từ header 4 byte.
    """
    return struct.unpack('>I', header_bytes)[0]