#valtyr
#pip package autoinstaller
#python autoinstaller.py

import subprocess
from terminal import colors as c

pip=[
    "pip",
    "install",
    "--upgrade",
    "--user",
    "pip"
]

packages=[
    "cryptography",
    "pycryptodome"
]

print('Running pip package autoinstaller...')
print('Interupting this process may cause unintentional damage...please be patient...')

print('Checking pip...')
try:
    subprocess.run(['pip','--version'])

except:
    print('No pip detected...aborting...')
    exit(1)

if(input('Upgrade pip? Y/N: ')=='y' or 'Y'):
    subprocess.run(pip)

print('Continuing execution...')

try:
    for package in packages:
        print(c.Bright_Cyan+'installing:\t'+package+c.White)
        try:
            subprocess.run(["pip", "install", package])
        except:
            print('ERR: Failed to install:\t'+package)
except:
    print('ERR: Unknown Interruption')

print(c.Bright_Green+'Autoinstaller has completed execution!'+c.White)
