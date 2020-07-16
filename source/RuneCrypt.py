#valtyr
import manipulator as m
from random import randint
import cryptoglyph
import encryptor
import decryptor
import argparse 
import getpass
import json

def get_available():
    return ['fernet','aes_eax','aes_cbc','arc2_eax','arc2_cbc','arc4']

def parse_encry(encry):
    if encry==None:
        available=get_available()
        count=0
        ops=[]
        while count != 15:
            ops.append(available[randint(0,len(available)-1)])
            count=count+1
        return ops
    else:
        return encry.split('-')

def encrypt(data,op,glyph):
    layer=cryptoglyph.layer()
    key=encryptor.get_general_key()

    if op=='random':
        op=get_available()
        op=randint(0,len(op)-1)

    if op=='fernet':
        key=encryptor.get_fernet_key()
        data=encryptor.fernet(key,data)
        layer.add_some(op,key)

    elif op=='aes_eax':
        data,tag,nonce=encryptor.aes_eax(key,data)
        layer.add_all(op,str(key),str(tag),str(nonce))
    
    elif op=='aes_cbc':
        data,iv=encryptor.aes_cbc(key,data)
        layer.add_some(op,key)
        layer.add_iv(iv)

    elif op=='arc2_eax':
        data,tag,nonce=encryptor.arc2_eax(key,data)
        layer.add_all(op,str(key),str(tag),str(nonce))

    elif op=='arc2_cbc':
        data,iv=encryptor.arc2_cbc(key,data)
        layer.add_some(op,key)
        layer.add_iv(iv)

    elif op=='arc4':
        data=encryptor.arc4(key,data)
        layer.add_some(op,str(key))

    else:
        print('Unknown Encryption Layer: Exiting...')
        exit(0)
    glyph.add_layer(layer)
    return data

def run_encry(password,data):
    glyph=cryptoglyph.glyph()
    glyph.password=password

    meta=str(args.raw_file).split('.')

    glyph.name=meta[0:len(meta)-1]
    glyph.file_format=meta[len(meta)-1]

    ops=parse_encry(args.encry)

    data=m.to_bytes(data)

    if args.decoy:
        fake_data=encryptor.get_random_bytes(len(data))
        fake_glyph=cryptoglyph.glyph()
        fake_glyph.password=password

    percent_total=len(ops)
    percent_current=1

    for op in ops:
        data=encrypt(data,str(op).lower(),glyph)           
        m.printProgressBar(percent_current,percent_total,prefix='Encrypting Data:',suffix='Complete',length=50)
        percent_current=percent_current+1

    m.write_data('rune.glyph',data)
    cryptoglyph.create_glyph(glyph)

    if args.decoy:
        percent_current=1
        for op in ops:
            fake_data=encrypt(fake_data,str(op).lower(),fake_glyph)
            m.printProgressBar(percent_current,percent_total,prefix='Encrypting Decoy:',suffix='Complete',length=50)
            percent_current=percent_current+1
        m.write_data('decoy/rune.glyph',fake_data)
    
    #Under Construction
    # if args.steg!=None:
    #     encryptor.steg(args.steg,data,str(args.gen).lower(),'steg/')
    #     print("rune.crypt hidden in\tsteg/"+str(args.steg))   
    #     if args.decoy:
    #         encryptor.steg(args.steg,fake_data,str(args.gen).lower(),'decoy/')
    #         print("decoy hidden in\t\tdecoy/"+str(args.steg))

    print('Secured crypto.glyph with password!')
    return True

def decrypt(key,data,op,tag,nonce,iv):
    if op=='fernet':
        return decryptor.fernet(key,data)
    elif op=='aes_eax':
        return decryptor.aes_eax(key,data,tag,nonce)
    elif op=='aes_cbc':
        return decryptor.aes_cbc(key,data,iv)
    elif op=='arc2_eax':
        return decryptor.arc2_eax(key,data,tag,nonce)
    elif op=='arc2_cbc':
        return decryptor.arc2_cbc(key,data,iv)
    elif op=='arc4':
        return decryptor.arc4(key,data)
    else:
        print('Unknown Decryption Layer: Exiting...')
        exit(0)
    return

def run_decry(password,crypto_glyph,raw_file):
    glyph=decryptor.parse_cryptoglyph(password,m.read_data(crypto_glyph))

    file_format=glyph['Format']
    file_name=glyph['Name']
    counter=int(glyph['Layers'])-1

    #TODO fix later
    # decryptor.steg('steg/test.jpg')

    data=m.read_data(raw_file)

    percent_total=counter+1
    percent_current=1
    while counter!=-1:
        layer='Layer-'+str(counter)
        key=glyph[layer]['key']
        op=glyph[layer]['op']
        tag=glyph[layer]['tag']
        nonce=glyph[layer]['nonce']
        iv=glyph[layer]['iv']
        data=decrypt(key,data,op,tag,nonce,iv)
        m.printProgressBar(percent_current,percent_total,prefix='Decrypting:',suffix='Complete',length=50)
        counter=counter-1
        percent_current=percent_current+1
    final_name=''.join(file_name)+'.'+file_format
    m.write_data(final_name,data)
    return True

parser = argparse.ArgumentParser(description='RuneCrypt : Hardcore Encryption')
parser.add_argument('-g',dest='glyph',action='store',default=None,help='Optional:Specify a json file to generate a crypto.glyph. Used to streamline RuneCrypt and ignore all cli args.')
parser.add_argument('-f',dest='raw_file',action='store',default=None,help='Used to flag a file for encryption/decryption. ex. -f example.txt or rune.glyph.')

parser.add_argument('-d',dest='decry',action='store',default=None,help='Flag used to signal the decryption operation : specify the path to crypto.glyph.')
parser.add_argument('-e',dest='encry',action='store',default=None,help='Optional:Specify encryption layers seperated by dashes. ex. random-random-random-random. Default uses 15 random layers. available layers:fernet, aes_eax, aes_cbc, arc2_eax, arc2_cbc, arc4')
parser.add_argument('-decoy',dest='decoy',action='store',nargs='?',default=False,const=True,help='Optional:Advanced:Signal that you want decoys made. This produces identical encrypted files of the same size, but with garbage data. The cryptoglyph for the decoy is not saved and the cryptoglyph for the real data cannot decrypt the decoy. ex. -decoy True or t.')
parser.add_argument('-huff',action='store',nargs='?',default=False,const=True,help='Optional:Advanced:Specify \'True\' to enable huffman encoding on the encrypted data to reduce final size. ex. -huff True or t.')
parser.add_argument('-s',dest='steg',action='store',default=None,help='Optional:Advanced:Specify a file/path to steganographically hide data. Can be a video.')
parser.add_argument('-gen',dest='gen',action='store',default=None,help='UNDER CONSTRUCTION Optional:Specify the steg generator used to hide the data. ex fib,era,ack,car')
parser.add_argument('-date',dest='date_lock',action='store',default=False,help='Optional:Advanced:Specify a date lock for crypto.glyph only allowing decryption on the specified date. ex.DD/MM/YYYY.')

args=parser.parse_args()

password=None

m.clear_terminal() 
m.print_title()
m.print_tip()

if args.glyph!=None:
    try:
        glyph=json.loads(m.read_data(str(args.glyph)))
        print('Glyph file loaded!')
    except:
        print('File Read Error: Glyph no loaded.')

    if glyph['password']!='':
        password=glyph['password']
    else:
        print('No password in glyph.')
        password=str(getpass.getpass('Password: '))

    if glyph['file']!='':
        args.raw_file=glyph['file']
    else:
        print('Bad file/file path in glyph.')
        exit(0)

    if glyph['layers']==['']:
        args.encry=None
    elif glyph['layers']!=['']:
        args.encry='-'.join(glyph['layers'])
    else:
        print('Bad encryption layers in glyph.')
        exit(0)

    if glyph['huff']!=False:
        args.huff=True
    else:
        args.huff=False

    if glyph['steg']!='':
        args.steg=glyph['steg']
    else:
        args.steg=None

    if glyph['gen']!='':
        args.gen=glyph['gen']
    else:
        args.gen=None

    if glyph['date']!='':
        args.date=glyph['date']
    else:
        args.date=None

    if glyph['decoy']!='':
        args.decoy=glyph['decoy']
    else:
        args.decoy=None

if args.raw_file == None:
    print('So uh...I need a file or data to encrypt/decrypt. Use -f for files or -d for raw data.')
    exit(0)
else:
    data=m.read_data(str(args.raw_file))
    
if password==None:
    password=getpass.getpass('Password: ')

if args.decry == None:
    if(run_encry(password,data)):
        print('Encryption Complete!')
else: #makes encryption the default action
    if(run_decry(password,args.decry,args.raw_file)):
        print('Decryption Complete!')            