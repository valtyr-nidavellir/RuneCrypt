#valtyr
from random import randint
from time import sleep

def read_file(file_name):
    data=None
    try:
        file=open(str(file_name),'r')
        data=file.readlines()
        file.close()
    except:
        print('ERR: Operation read_file failed with args: '+str(file_name))
        exit(0)
    return data

def read_data(file_name):
    data=None
    try:
        file=open(str(file_name),'rb')
        data=file.read()
        file.close()
    except:
        print('ERR: Operation read_data failed with args:\t'+file_name)
        exit(0)
    return data

def write_file(file_name,data):
    try:
        file=open(file_name,'w')
        file.writelines(data)
        file.close()
    except:
        print('ERR: Operation write_data failed with args: '+str(file_name))

def write_data(file_name,data):
    try:
        file=open(file_name,'wb')
        file.write(data)
        file.close()
    except:
        print('ERR: Operation write_data failed with args: '+str(file_name))

def to_bytes(data):
    if type(data)!=bytes:
        try:
            return str.encode(data)
        except:
            return data
    else:
        return data

def detect_gpu():
    # add conda numba libs to detect a and return gpu
    return 