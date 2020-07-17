#valtyr
from random import randint
from time import sleep
import os

def read_file(file_name):
    data=None
    try:
        file=open(str(file_name),'r')
        data=file.readlines()
        file.close()
    except:
        print('ERR: File Read Failed:\t'+file_name)
        exit(0)
    return data

def read_data(file_name):
    data=None
    try:
        file=open(str(file_name),'rb')
        data=file.read()
        file.close()
    except:
        print('ERR: File Read Failed:\t'+file_name)
        exit(0)
    return data

def write_file(file_name,data):
    file=open(file_name,'w')
    file.writelines(data)
    file.close()

def write_data(file_name,data):
    file=open(file_name,'wb')
    file.write(data)
    file.close()

def to_bytes(data):
    if type(data)!=bytes:
        try:
            return str.encode(data)
        except:
            return data
    else:
        return data

def to_string(data):
    if type(data)==bytes:
        return data.decode()
    else:
        return data

def to_literal(data):
    return 

def print_title():
    for line in read_file('data/title.txt'):
        sleep(0.07)
        print(line.strip('\n'))

def print_tip():
    tips=[
        'The crypto.glyph file is the weakest link in the encryption chain. Protect it carefully.',
        'Decoys can be generated using -decoy t. The decoy rune.glyph is the same size as the original but filled with garbage data.',
        'You can use the included autoinstaller.py to upgrade pip and RuneCrypt\'s dependencies.',
        'Some generated MAC\'s can fail an eax check, so these will be auto corrected during runtime.',
        'You can use the included glyph.json file to streamline the command line args. Use -g glyph.json to load the file\'s args.',
        'The encryption algo arc2_eax is not included in the default rotation for the default 10 random layers due to MAC failure when dealing with larger data.',
    ]
    print('Tip: '+tips[randint(0,len(tips)-1)])
    
def clear_terminal():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix}\t|{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()