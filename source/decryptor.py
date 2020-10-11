#valtyr
from cryptography.fernet import Fernet
from Crypto.Util.Padding import unpad
from Crypto.Cipher import ARC2
from Crypto.Cipher import ARC4
from Crypto.Cipher import AES
import encryptor
import stegano
import json

# add gpu exceleration to all functions

def parse_cryptoglyph(password,data):
    try:
        return json.loads(arc4(encryptor.get_hashed_pass(password).encode(),data))
    except:
        print('Incorrect Password!')
        exit(0)

def eval_aspects(key,tag,nonce):
    return eval(key),eval(tag),eval(nonce)

def fernet(key,data):
    cipher=Fernet(eval(key))
    return cipher.decrypt(data)

def aes_eax(key,data,tag,nonce):
    key,tag,nonce=eval_aspects(key,tag,nonce)
    cipher=AES.new(key,AES.MODE_EAX,nonce)
    try:
        return cipher.decrypt_and_verify(data,tag)
    except(ValueError):
        print('Decryption Failed: MAC check failed.')
        exit(0)
    return 

def aes_cbc(key,data,iv):
    key=eval(key)
    iv=eval(iv)
    cipher=AES.new(key,AES.MODE_CBC,iv)
    return unpad(cipher.decrypt(data),AES.block_size)

def arc2_eax(key,data,tag,nonce):
    key,tag,nonce=eval_aspects(key,tag,nonce)
    cipher=ARC2.new(key,ARC2.MODE_EAX,nonce)
    try:
        return cipher.decrypt_and_verify(data,tag)
    except(ValueError):
        print('Decryption Failed: MAC check failed.')
        exit(0)
    return

def arc2_cbc(key,data,iv):
    key=eval(key)
    iv=eval(iv)
    cipher=ARC2.new(key,ARC2.MODE_CBC,iv)
    return unpad(cipher.decrypt(data),ARC2.block_size)

def arc4(key,data):
    try:
        cipher=ARC4.new(eval(key))
    except:
        cipher=ARC4.new(key)
    return cipher.decrypt(data)

def steg(name):
    #Under Construction - might shell stegano or steghide
    print('Retrieving steg data...this might take a moment...')
    print(stegano.lsb.reveal(name))
    return