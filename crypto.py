from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

key = b'\xbc\x96(WA\x82\n\xfbh\x80\xcb\xb2<\x1d\xfea'
iv = b"\xef\xd1\xf4G'T\xb8\x10\xa3w<L\x08\xa0;\x96"

def encryption(plaintext):
    plaintext = bytes(plaintext, 'utf-8')
    cipher = AES.new(key,AES.MODE_CBC,iv)
    text = cipher.encrypt(pad(plaintext,16))
    return text.hex()

def decryption(ciphertext):
    ciphertext = bytes.fromhex(ciphertext)
    decipher = AES.new(key,AES.MODE_CBC,iv)
    text = unpad(decipher.decrypt(ciphertext),block_size=16)
    return text.decode('utf-8') 

# text = 'sasank world'

# encrypted = encryption(text)
# print(encrypted)

# decrypted = decryption(encrypted)
# print(decrypted)