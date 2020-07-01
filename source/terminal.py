#valtyr
import os

def clear_terminal():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        pass

def reset_color():
    print(colors.White)

class colors:
    Black=  '\u001b[30m'
    Red=    '\u001b[31m'
    Green=  '\u001b[32m'
    Yellow= '\u001b[33m'
    Blue=   '\u001b[34m'
    Magenta='\u001b[35m'
    Cyan=   '\u001b[36m'
    White=  '\u001b[37m'
    Bright_Black=   '\u001b[30;1m'
    Bright_Red=     '\u001b[31;1m'
    Bright_Green=   '\u001b[32;1m'
    Bright_Yellow=  '\u001b[33;1m'
    Bright_Blue=    '\u001b[34;1m'
    Bright_Magenta= '\u001b[35;1m'
    Bright_Cyan=    '\u001b[36;1m'

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()