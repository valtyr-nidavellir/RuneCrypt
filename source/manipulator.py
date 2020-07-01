#valtyr
import terminal

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
        print(terminal.colors.Bright_Red+line.strip('\n'))
    terminal.reset_color()