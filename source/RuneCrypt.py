#valtyr
import manipulator as m
import terminal as term
import encryptor
import decryptor
import cryptoglyph
import argparse 
import json
from random import randint
import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
import webbrowser


def get_available_ops():
    return ['fernet','aes_eax','arc2_eax','arc4']

def parse_encry(encry):
    if encry==None:
        #default layering
        available_ops=get_available_ops()
        op_count=0
        ops=[]
        while op_count != 50:
            ops.append(available_ops[randint(0,len(available_ops)-1)])
            op_count=op_count+1
        return ops
    else:
        return encry.split('-')

def encrypt(data,op,glyph):

    if op=='random':
        op=get_available_ops()
        op=randint(0,len(op)-1)

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

    meta=str(args.raw_file).split('.')

    glyph.name=meta[0:len(meta)-1]
    glyph.file_format=meta[len(meta)-1]

    ops=parse_encry(args.encry)

    data=m.to_bytes(data)

    if(args.decoy):
        fake=encryptor.get_random_bytes(len(data))
        fake_glyph=cryptoglyph.glyph()
        fake_glyph.password=args.password

    percent_total=len(ops)
    percent_current=1
    for op in ops:
        data=encrypt(data,str(op).lower(),glyph)           
        term.printProgressBar(percent_current,percent_total,prefix='Encrypting Data:',suffix='Complete',length=50)
        percent_current=percent_current+1

    if(args.decoy):
        percent_current=1
        for op in ops:
            fake=encrypt(fake,str(op).lower(),fake_glyph)
            term.printProgressBar(percent_current,percent_total,prefix='Encrypting Decoy:',suffix='Complete',length=50)
            percent_current=percent_current+1
        m.write_data('decoy/rune.glyph',fake)

    m.write_data('rune.glyph',data)
    print('Securing crypto.glyph with password...')
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
    file_name=glyph['Name']
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
    final_name=''.join(file_name)+'.'+file_format
    m.write_data(final_name,data)
    return True

def open_doc():
    #TODO: Change the link to git webpages for runecrypt info site
    webbrowser.open('https://github.com/valtyr-nidavellir/')

def execute():
    return 

parser = argparse.ArgumentParser(description='RuneCrypt : Hardcore Encryption')
#under construction
# parser.add_argument('gui',action='store',nargs='?',default=False,const=True,help='Used to open the GUI version of RuneCrypt. Useful for first timers.')
parser.add_argument('-g',dest='glyph',action='store',default=None,help='Optional:Specify a json file to generate a crypto.glyph. Used to streamline RuneCrypt and ignore all cli args.')
parser.add_argument('-f',dest='raw_file',action='store',default=None,help='Used to flag a file for encryption/decryption. ex. -f example.txt or rune.glyph.')

parser.add_argument('-d',dest='decry',action='store',default=None,help='Flag used to signal the decryption operation : specify the path to crypto.glyph.')
parser.add_argument('-e',dest='encry',action='store',default=None,help='Optional:Specify encryption layers seperated by dashes. ex. random-random-random-random. Default uses 50 random layers.')
parser.add_argument('-p',dest='password',action='store',default=None,help='Specify a password used to encrypt/decrypt a crypto.glyph.')

parser.add_argument('-decoy',dest='decoy',action='store',nargs='?',default=False,const=True,help='Optional:Advanced:Signal that you want decoys made. This produces identical encrypted files of the same size, but with garbage data. The cryptoglyph for the decoy is not saved and the cryptoglyph for the real data cannot decrypt the decoy. ex. -decoy True or t.')
parser.add_argument('-s',dest='steg_file',action='store',default=False,help='Optional:Advanced:Specify a file/path to steganographically hide data. Can be a video.')
parser.add_argument('-huff',action='store',nargs='?',default=False,const=True,help='Optional:Advanced:Specify \'True\' to enable huffman encoding on the encrypted data to reduce final size. ex. -huff True or t.')
parser.add_argument('-date',dest='date_lock',action='store',default=False,help='Optional:Advanced:Specify a date lock for crypto.glyph only allowing decryption on the specified date. ex.DD/MM/YYYY.')

args=parser.parse_args()

term.clear_terminal() 
colors=term.colors

global img
#use glyph here to skip all flag checks 

if args.glyph != None:
    glyph=m.read_file(str(args.glyph))
    print(colors.Bright_Cyan+'Glyph file loaded!'+colors.White)
    #add glyph load for args

else:
    if args.gui=='gui':
        #TODO: opens when decoy is signaled for some reason

        #launch gui version
        window=tk.Tk()
        window.iconbitmap('data/valtyr.ico')
        window.configure(bg='black')
        img=ImageTk.PhotoImage(Image.open("title_img.png"))
        title=tk.Label(window,image=img,borderwidth=0,highlightthickness=0)
        title.place(x=5,y=0)
        font=font.Font(size=30)

        #encry btn
        btn_encry=tk.Button(window,borderwidth=0,highlightthickness=0,text='Encrypt',bg="#121212",fg="#e60000")
        btn_encry['font']=font
        btn_encry.place(x=20,y=450)

        #decry btn
        btn_decry=tk.Button(window,borderwidth=0,highlightthickness=0,text='Decrypt',bg="#121212",fg="#e60000")
        btn_decry['font']=font
        btn_decry.place(x=200,y=450)

        #information btn
        btn_info=tk.Button(window,command=open_doc,borderwidth=0,highlightthickness=0,text='Documentation',bg="#121212",fg="#e60000")
        btn_info['font']=font
        btn_info.place(x=380,y=450)

        #command-line width=175,height=2,
        command_line=tk.Label(window,width=52,borderwidth=0,highlightthickness=0,text='Current Command: ',bg="#121212",fg="#e60000")
        command_line.place(x=20,y=550)
        command_line['font']=font

        btn_info=tk.Button(window,command=execute,borderwidth=0,highlightthickness=0,text='Execute',bg="#121212",fg="#e60000")
        btn_info['font']=font
        btn_info.place(x=20,y=600)

        window.geometry("1240x800")
        window.mainloop()
    else:
        m.print_title()
        raw_data=None 

        if args.raw_file == None:
            print(colors.Bright_Red+'So uh...I need a file or data to encrypt/decrypt. Use -f for files or -d for raw data.'+colors.White)
            exit(0)
        else:
            data=m.read_data(str(args.raw_file))
            

        if args.password==None:
            print(colors.Bright_Red+'I need a password to encrypt/decrypt the crypto.glyph! Use -p {password}.'+colors.White)
            exit(0)

        if args.decry == None:
            if(run_encry(data)):
                print('Encryption Complete!')
        else: #makes encription the default action
            if(run_decry(args.decry,args.raw_file)):
                print('Decryption Complete!')

#DATE LOCK PROTOTYPE
# accept date through arg
# add to the password then hash
# in decrypting check system date against ntp date
# if different refuse decryption
# if same try decrypt with date appended to pass and hashed
# if fail then try password hash only              
    