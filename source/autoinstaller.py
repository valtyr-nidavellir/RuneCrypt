#valtyr
#python autoinstaller.py

import subprocess

pip=[
    "python3",
    "-m",
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
]

print('Running pip package autoinstaller...')
print('Interupting this process may cause unintentional damage...please be patient...')

print('Checking pip...')
try:
    subprocess.run(['python3','-m','pip','--version'])

except:
    print('No pip detected...aborting...')
    exit(1)

choice=input('Upgrade pip? Y/N: ')
if(choice.lower()=='y'):
    print("Upgrading.")
    subprocess.run(pip)

print('Continuing execution...')

try:
    for package in packages:
        print('Installing:\t'+package)
        try:
            subprocess.run(["python3","-m","pip","install", package])
        except:
            print('ERR: Failed to install:\t'+package)
except:
    print('ERR: Unknown Interruption')

print('Autoinstaller has completed execution!')
