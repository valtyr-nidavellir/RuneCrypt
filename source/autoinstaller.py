#valtyr
#pip package autoinstaller
#python autoinstaller.py

import subprocess

pip=[
    "pip",
    "install",
    "--upgrade",
    "--user",
    "pip"
]

packages=[
    "cryptography",
    "pycryptodome",
    "stegano",
    "pillow"
]

print('Running pip package autoinstaller...')
print('Interupting this process may cause unintentional damage...please be patient...')

print('Checking pip...')
try:
    subprocess.run(['pip','--version'])

except:
    print('No pip detected...aborting...')
    exit(1)

choice=input('Upgrade pip? Y/N: ')
if(choice=='y' or choice=='Y'):
    subprocess.run(pip)

print('Continuing execution...')

try:
    for package in packages:
        print('installing:\t'+package)
        try:
            subprocess.run(["pip", "install", package])
        except:
            print('ERR: Failed to install:\t'+package)
except:
    print('ERR: Unknown Interruption')

print('Autoinstaller has completed execution!')
