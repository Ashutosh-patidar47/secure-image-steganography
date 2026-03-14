from Crypto.Cipher import AES
import hashlib
import base64


def pad(text):
    while len(text) % 16 != 0:
        text += " "
    return text


def encrypt_message(message, password):

    key = hashlib.sha256(password.encode()).digest()

    cipher = AES.new(key, AES.MODE_ECB)

    encrypted = cipher.encrypt(pad(message).encode())

    return base64.b64encode(encrypted).decode()


def decrypt_message(encrypted_message, password):

    key = hashlib.sha256(password.encode()).digest()

    cipher = AES.new(key, AES.MODE_ECB)

    decoded = base64.b64decode(encrypted_message)

    decrypted = cipher.decrypt(decoded)

    return decrypted.decode().strip()