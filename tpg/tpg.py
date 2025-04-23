import keyboard
import os
import time

def listgr(unitperedvogenielist:list,kastcor='>',title='')->str:
    cursor=0
    while True:
        cor=''
        print(title)
        if keyboard.is_pressed('down'):
            cursor=cursor+1
        if keyboard.is_pressed('up'):
            cursor=cursor-1
        if cursor<0:
            cursor=0
        for i in range(0,len(unitperedvogenielist)):
            if cursor==i:
                cor=kastcor
            else:
                cor=''
            print(cor+unitperedvogenielist[i])
        if keyboard.is_pressed('enter'):
            unitperedvogenie=unitperedvogenielist[cursor]
            while keyboard.is_pressed('enter'):
                time.sleep(0.1)
                pass
            return unitperedvogenie
        os.system('clear') 
        
class ansi:
    def __init__(self):
        self.stule={
            'standart':0,
            'big':1,
            'tone':2,
            'kursive':3,
            'line':4,
            'mercanie':5
        }
        self.color={
            'blak':30,
            'red':31,
            'green':32,
            'yelou':33,
            'blue':34,
            'violet':35,
            'beruza':36,
            'white':37,
            'clear':0
        }
        self.beggraubd={
            'blak':40,
            'red':41,
            'green':42,
            'yelou':43,
            'blue':44,
            'violet':45,
            'beruza':46,
            'white':47,
            'clear':0
            
        }
def color(stule,color,begraund)->str:#stule,color,beggraubd
    #if len(ansis)>3:
    #    
    self=ansi()
    try:
        stule=self.stule[stule]
    except KeyError:
        raise KeyError(f'error Not correct parameters , parameters :{self.stule.keys()} ')
    try:
        color=self.color[color]
    except KeyError:
        raise KeyError(f'error Not correct parameters , parameters :{self.color.keys()} ')
    try:
        begraund=self.beggraubd[begraund]
    except KeyError:
        raise KeyError(f'error Not correct parameters , parameters :{self.beggraubd.keys()} ')
    return f'\33[{stule};{color};{begraund}m'

def cursor(x:int,y:int,text:str)->str:
    if y>0:
        print(f"\033[{y}A{text}")#в верх
    else:
        print(f"\033[{y}B{text}")#в низ
    if x>0:
        print(f"\033[{x}C{text}")#в перед 
    else:
        print(f"\033[{x}D{text}")# на зад
        
def clear():
    print("\033[2J") #очистка 
    os.system("clear")
    
def yes_ro_no(text:str,kastcor='>',yestxt='yes',notxt='no'):
    out=False
    yes=''
    no='>'
    while True:
        print('\n'*13)
        if keyboard.is_pressed('left'):
            yes=kastcor
            no=''
            out=True
        if keyboard.is_pressed('right'):
            no=kastcor
            yes=''
            out=False
        if keyboard.is_pressed('enter'):
            while keyboard.is_pressed('enter'):
                time.sleep(0.1)
                pass
            return out
        print(' '*(10-len(text))+text)
        print(f'{' '*15}{yes}{yestxt} {no}{notxt}')
        os.system('clear')
        
        
def cursor(x:int,y:int,text:str)->str:
    if y >0:
        print(f"\033[{y}A{text}")#в верх
    else:
        print(f"\033[{y}B{text}")#в низ
    if x>0:
        print(f"\033[{x}C{text}")#в перед 
    else:
        print(f"\033[{x}D{text}")# на зад
        
def clear():
    print("\033[2J"+'\033[0') #очистка 
    os.system("clear")

        
