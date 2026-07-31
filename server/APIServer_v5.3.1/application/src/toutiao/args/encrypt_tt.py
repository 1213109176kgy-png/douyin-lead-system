import base64
import hashlib

from Crypto.Cipher import AES


def encrypt_key(logid, seed):
    key = (logid + seed + logid)
    return hashlib.md5(key).hexdigest()


def aes_cbc_decrypt(text_base64, secret_key):
    key = bytes.fromhex(secret_key)
    iv = key[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = base64.b64decode(text_base64)
    decrypted_data = cipher.decrypt(encrypted_data)
    padding_len = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_len]
    return decrypted_data.decode('utf-8')

