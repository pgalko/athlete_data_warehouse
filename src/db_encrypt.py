import Crypto.Random
from Crypto.Cipher import AES
import hashlib

def generate_key(password, salt, iterations):
    assert iterations > 0
    key = password + salt.decode('latin-1')
    key = key.encode()
    for i in range(iterations):
        key = hashlib.sha256(key).digest()  
    return key

def pad_text(text, multiple):
    extra_bytes = len(text) % multiple
    padding_size = multiple - extra_bytes
    padding = chr(padding_size) * padding_size
    padded_text = text + padding
    return padded_text.encode()

def unpad_text(padded_text):
    padded_text = padded_text.decode()
    padding_size = ord(padded_text[-1])
    text = padded_text[:-padding_size]
    return text

def str2md5(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()   

