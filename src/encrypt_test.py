import Crypto.Random
from Crypto.Cipher import AES
import hashlib
import base64

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

#----Crypto Variables----
# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 2000 # PG:Consider increasing number of iterations
# the size multiple required for AES
AES_MULTIPLE = 16

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    #iv = Crypto.Random.get_random_bytes(AES.block_size)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]
    #iv = ciphertext[:AES.block_size]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB) #PG: Consider changing to MODE_CBC
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext 

encrypted_string = base64.b64encode(encrypt("Palo Galko", "00000"))
encrypted_string = encrypted_string.decode('utf-8')
print(encrypted_string)

decrypted_string = decrypt(base64.b64decode(encrypted_string), '00000')
print(decrypted_string)

