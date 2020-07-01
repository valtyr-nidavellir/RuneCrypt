#valtyr
from cryptography.fernet import Fernet
from Crypto.Cipher import AES
from Crypto.Cipher import Blowfish
from Crypto import Random
from random import choice
import manipulator as m
import json


def fernet(key,data):
    cipher=Fernet(key)
    return cipher.encrypt(data)

def get_fernet_key():
    return Fernet.generate_key() 

def aes(key,data):
    cipher = AES.new(key, AES.MODE_EAX)
    data,tag=cipher.encrypt_and_digest(data)  
    return data,tag,cipher.nonce

def get_aes_key():
    sizes=[16,24,32]
    return Random.get_random_bytes(choice(sizes))

def blowfish():
    return

def get_blowfish_key():
    return 
