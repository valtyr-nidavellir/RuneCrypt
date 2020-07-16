#valtyr
from cryptography.fernet import Fernet
from stegano.lsbset import generators
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Cipher import ARC2
from Crypto.Cipher import ARC4
from Crypto.Hash import SHA256
from Crypto import Random
from random import choice
import manipulator as m
import stegano
import json

def get_general_key():
    return Random.get_random_bytes(choice([16,24,32]))

def get_random_bytes(size):
    return Random.get_random_bytes(size)

def get_hashed_pass(password):
    return SHA256.new(str.encode(password)).hexdigest()

def secure_glyph(password,data):
    hashed=get_hashed_pass(password)
    data=arc4(hashed.encode(),data)
    m.write_data('crypto.glyph',data)
    return True

def fernet(key,data):
    cipher=Fernet(key)
    return cipher.encrypt(data)

def get_fernet_key():
    return Fernet.generate_key() 

    
def aes_eax(key,data):
    cipher=AES.new(key, AES.MODE_EAX)
    data,tag=cipher.encrypt_and_digest(data)  
    return data,tag,cipher.nonce

def aes_cbc(key,data):
    cipher=AES.new(key,AES.MODE_CBC)
    return cipher.encrypt(pad(data,AES.block_size)),cipher.iv
    

def arc2_eax(key,data):
    cipher=ARC2.new(key,ARC2.MODE_EAX)
    data,tag=cipher.encrypt_and_digest(data)
    return data,tag,cipher.nonce

def arc2_cbc(key,data):
    cipher=ARC2.new(key,ARC2.MODE_CBC)
    return cipher.encrypt(pad(data,ARC2.block_size)),cipher.iv

def arc4(key,data):
    cipher=ARC4.new(key)
    return cipher.encrypt(data)

#Under Construction
def steg(file_path,data,gen,path):
    if gen=='fib':
        generator=generators.fibonacci()
    elif gen=='era':
        generator=generators.eratosthenes()
    elif gen=='ack':
        generator=generators.ackermann(10)
    elif gen=='car':
        generator=generators.carmichael()
    else:
        pass
        # print('Steg Failed: Unknown Steg Generator.')
        # exit(0)

    try:
        picture=stegano.lsb.hide(file_path,data)
        picture.save(path+file_path)
    except Exception as e:
        print('Steg Failed: '+str(e))
        exit(0)
    return