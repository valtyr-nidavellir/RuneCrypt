from cryptography.fernet import Fernet
from Crypto.Cipher import AES
import json

def parse_cryptoglyph(data):
    data=json.loads(data)
    return data

def fernet(key,data):
    cipher=Fernet(key)
    return cipher.decrypt(data)

def aes(key,data,tag,nonce):
    key=eval(key)
    tag=eval(tag)
    nonce=eval(nonce)
    cipher=AES.new(key,AES.MODE_EAX,nonce)
    return cipher.decrypt_and_verify(data,tag)