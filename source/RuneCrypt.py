#valtyr
import manipulator as m
import terminal as term
import encryptor
import decryptor
import cryptoglyph
import argparse 
import json
from random import randint

def parse_encry(encry):
    if encry==None:
        #default layering
        available_ops=['fernet','aes_eax','arc2_eax','arc4']
        op_count=0
        ops=[]
        while op_count != 70:
            ops.append(available_ops[randint(0,len(available_ops)-1)])
            op_count=op_count+1
        return ops
    else:
        return encry.split('-')

def encrypt(data,op,glyph):
    if op=='fernet':
        layer=cryptoglyph.layer()
        key=encryptor.get_fernet_key()
        data=encryptor.fernet(key,data)
        layer.add_some(op,key)
        glyph.add_layer(layer)

    elif op=='aes_eax':
        layer=cryptoglyph.layer()
        key=encryptor.get_general_key()
        data,tag,nonce=encryptor.aes_eax(key,data)
        layer.add_all(op,str(key),str(tag),str(nonce))
        glyph.add_layer(layer)

    elif op=='arc2_eax':
        layer=cryptoglyph.layer()
        key=encryptor.get_general_key()
        data,tag,nonce=encryptor.arc2_eax(key,data)
        layer.add_all(op,str(key),str(tag),str(nonce))
        glyph.add_layer(layer)

    elif op=='arc4':
        layer=cryptoglyph.layer()
        key=encryptor.get_general_key()
        data=encryptor.arc4(key,data)
        layer.add_some(op,str(key))
        glyph.add_layer(layer)

    else:
        no='match'
        #random
    return data

def run_encry(data):
    glyph=cryptoglyph.glyph()
    glyph.password=args.password
    glyph.file_format=str(args.raw_file).split('.')[len(str(args.raw_file).split('.'))-1]
    ops=parse_encry(args.encry)
    data=m.to_bytes(data)
    percent_total=len(ops)
    percent_current=1
    for op in ops:
        data=encrypt(data,str(op).lower(),glyph)
        term.printProgressBar(percent_current,percent_total,prefix='Encrypting:',suffix='Complete',length=50)
        percent_current=percent_current+1

    m.write_data('rune.glyph',data)#change later 
    
    cryptoglyph.create_glyph(glyph)
    return True

def decrypt(key,data,op,tag,nonce):
    if op=='fernet':
        return decryptor.fernet(key,data)
    elif op=='aes_eax':
        return decryptor.aes_eax(key,data,tag,nonce)
    elif op=='arc2_eax':
        return decryptor.arc2_eax(key,data,tag,nonce)
    elif op=='arc4':
        return decryptor.arc4(key,data)
    else:
        do='nothing'
    return

def run_decry(crypto_glyph,raw_file):
    #read crypto.glyph and prompt for password 
    glyph=decryptor.parse_cryptoglyph(args.password,m.read_data(crypto_glyph))

    file_format=glyph['Format']
    counter=int(glyph['Layers'])-1

    data=m.read_data(raw_file)

    percent_total=counter+1
    percent_current=1
    while counter!=-1:
        layer='Layer-'+str(counter)
        key=glyph[layer]['key']
        op=glyph[layer]['op']
        tag=glyph[layer]['tag']
        nonce=glyph[layer]['nonce']
        data=decrypt(key,data,op,tag,nonce)
        term.printProgressBar(percent_current,percent_total,prefix='Decrypting:',suffix='Complete',length=50)
        counter=counter-1
        percent_current=percent_current+1
    file_name='result.'+file_format
    m.write_data(file_name,data)
    return True


parser = argparse.ArgumentParser(description='RuneCrypt : Hardcore Encryption')
parser.add_argument('-f',dest='raw_file',action='store',default=None,help='Used to flag a file for encryption/decryption. ex. example.txt')
parser.add_argument('-data',dest='raw_data',action='store',default=None,help='Used to flag raw data for encryption/decryption rather than a file. ex. blahblahblah')

parser.add_argument('-d',dest='decry',action='store',default=None,help='Flag used to signal the decryption operation : specify the path to crypto.glyph')
parser.add_argument('-e',dest='encry',action='store',default=None,help='Optional:Specify encryption layers seperated by dashes. ex. random-random-random-random. Default uses 10 random layers.')
parser.add_argument('-p',dest='password',action='store',default=None,help='Specify a password used to encrypt/decrypt a crypto.glyph.')

parser.add_argument('-g','-glyph',dest='glyph',action='store',default=None,help='Optional:Specify a json file to generate a crypto.glyph. Used to streamline RuneCrypt and ignore -e and -p args.')
parser.add_argument('-steg',dest='steg_file',action='store',default=False,help='Optional:Advanced:Specify a file/path to steganographically hide data. Can be a video.')
parser.add_argument('-huff',dest='human',action='store',default=False,help='Optional:Advanced:Specify \'True\' to enable huffman encoding on the encrypted data to reduce final size.')
parser.add_argument('-date',dest='date_lock',action='store',default=False,help='Optional:Advanced:Specify a date lock for crypto.glyph only allowing decryption on the specified date. ex.DD/MM/YYYY.')

args=parser.parse_args()

term.clear_terminal()
m.print_title()

colors=term.colors
raw_data=None

#use glyph here to skip all flag checks 

if args.glyph != None:
    glyph=m.read_file(str(args.glyph))
    print(colors.Bright_Cyan+'Glyph file loaded! Encrypting...'+colors.White)
    #add glyph load for args

else:
    if args.raw_file == None and args.raw_data == None:
        print(colors.Bright_Red+'So uh...I need a file or data to encrypt/decrypt. Use -f for files or -d for raw data.'+colors.White)
        exit(0)
    else:
        if args.raw_file!=None:
            data=m.read_data(str(args.raw_file))
        else:
            data=str(args.raw_data)

    if args.password==None:
        print(colors.Bright_Red+'I need a password to encrypt/decrypt the crypto.glyph! Use -p {password}.'+colors.White)
        exit(0)

    if args.decry == None:
        if(run_encry(data)):
            print('Encryption Complete!')
    else: #makes encription the default action
        if(run_decry(args.decry,args.raw_file)):
            print('Decryption Complete!')
    