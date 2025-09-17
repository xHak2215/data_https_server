import json
import os
import time
import sys
import threading
import sys

from .ansi import  ansi,art

import keyboard

def listgr(unitperedvogenielist:list,kastcor='>',title='',style='standart',ansi='\033[0m')->str:
    cursor=0
    while True:
        cor=''
        print(title)
        if keyboard.is_pressed('esc'):
            return None
        if keyboard.is_pressed('down'):
            cursor=cursor+1
        if keyboard.is_pressed('up'):
            cursor=cursor-1
        if cursor<0:
            cursor=0
        if cursor>len(unitperedvogenielist)-1:
            cursor=len(unitperedvogenielist)-1
        for i in range(len(unitperedvogenielist)):
            if style =='standart':
                if cursor==i:
                    cor=kastcor
                else:
                    cor=' '
                print(ansi+cor+str(unitperedvogenielist[i]))
            elif style=='scob':
                if cursor==i:
                    cor='+'
                else:
                    cor=''
                prob=' '*(max(0,15-len(str(unitperedvogenielist[i]))))
                print(ansi+f'{str(unitperedvogenielist[i])}{prob}({cor})')
            else:
                raise SyntaxError('no style'+style)
            #if type(unitperedvogenielist[i])=="dict":
            #    for a in unitperedvogenielist[i].keys():
            #        print('  '+cor+a+'ᐁ')
            #        for s in a:
            #            print(s)
        if keyboard.is_pressed('enter'):
            unitperedvogenie=unitperedvogenielist[cursor]
            while keyboard.is_pressed('enter'):
                time.sleep(0.1)
            return unitperedvogenie
        if os.name == 'nt': 
            os.system("cls")
        else:
            os.system("clear")
        
def settings(data:dict,kastcor='>',title='',style='zapoln',jsonf=None,ansi='\033[0')->str:
    cursor=0
    if os.path.isfile(jsonf):
            with open(jsonf, "r") as json_settings:
                data = json.load(json_settings)
    else:
        raise FileNotFoundError(f'no faile ({jsonf})')
    while True:
        cor=''
        print(title)
        if keyboard.is_pressed('esc'):
            with open(jsonf, "w") as json_settings:
                json_settings.write(json.dumps(data))
            while keyboard.is_pressed('esc'):
                time.sleep(0.1)
            return data
        if keyboard.is_pressed('down'):
            cursor=cursor+1
        if keyboard.is_pressed('up'):
            cursor=cursor-1
        if cursor<0:
            cursor=0
        if cursor>len(list(data.keys()))-1:
            cursor=len(list(data.keys()))-1
        for i in range(len(list(data.keys()))):
            punkt=list(data.keys())[i]
            if cursor==i:
                cor=kastcor
            else:
                cor=' '
            if style == 'zapoln':
                if bool(data[punkt]):
                    flag='█'
                else:
                    flag='░'
            elif style == '+':
                if bool(data[punkt]):
                    flag='+'
                else:       
                    flag='-'
            print(ansi+cor+punkt+ ' ' * int(20 - len(punkt)) +'['+flag+']')
        if keyboard.is_pressed('enter'):
            if data[list(data.keys())[cursor]]:
                data[list(data.keys())[cursor]]=False
            else:
                data[list(data.keys())[cursor]]=True
            while keyboard.is_pressed('enter'):
                time.sleep(0.1)
        if os.name == 'nt': 
            os.system("cls")
        else:
            os.system("clear")
        
def terminal_size() ->list:
    """
    terminal size
    
    Returns:
        list: 0 - height. 1 - lines num
    """
    # X , Y 
    return [int(os.get_terminal_size().columns) , int(os.get_terminal_size().lines)]

def color(text,color,stule='standart',begraund='blak',end='\33[0m')->str:#text,color,stule,beggraubd
    r"""позволяет перекрашивать цвет работает на `ansi`

    Args:
        text (_str_): текст который будет перекрашен
        color (_srt_): цвет текста
        stule (str, optional): стиль. Defaults to 'standart'.
        begraund (str, optional): задний фон. Defaults to 'blak'.
        end (str, optional): конец строки. Defaults to '\33[0'.

    Returns:
        str: текст с `ansi` кодами
    """
    
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
    return f"\33[{stule};{color};{begraund}m{text}{end}"
    
def yes_ro_no(text:str,kastcor='>',yestxt='yes',notxt='no',midst=False):
    out=False
    yes=''
    no='>'
    otst=0
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
        if midst:otst=round(terminal_size()[0]/2)
        print(' '*otst+text)
        print(f'{' '*otst}{yes}{yestxt} {no}{notxt}')
        if os.name == 'nt': 
            os.system("cls")
        else:
            os.system("clear")
        

def cursor(x:int,y:int,display='█',fone=' ')->str:
    print(('\n'*y)+(fone*x+display))
    
    
'''
if y > 0:
    print(f"\033[{y}Am{text}")#в верх
else:
    print(f"\033[{y}Bm{text}")#в низ
if x > 0:
    print(f"\033[{x}Cm{text}")#в перед 
else:
    print(f"\033[{x}Dm{text}")# на зад
'''           
        
def clear():
    #print('\033[0m') #очистка цвета
    if os.name == 'nt': 
        os.system("cls")
    else:
        os.system("clear")

def ramka(text):
    text=str(text)
    ots=' '*(int(round(terminal_size()[0]/2))-int(len(text)+2))
    return f'{ots}╔{'═'*len(text)}╗\n{ots}║{text}║\n{ots}╚{'═'*len(text)}╝'

class InputMany:
    def __init__(self):
        self.output = []
        self.lock = threading.Lock()  # Для безопасного доступа к output
    
    def input_at(self, x: int, y: int, prompt: str): 
        """Создает поле ввода в указанных координатах"""
        # Перемещаем курсор и выводим приглашение
        with self.lock:
            sys.stdout.write(f"\033[{y};{x}H{prompt}")
            input_pos = x + len(prompt)
            sys.stdout.write(f"\033[{y};{input_pos}H")
            sys.stdout.flush()
        
        # Читаем ввод
        user_input = sys.stdin.readline()
        
        # Сохраняем результат
        with self.lock:
            self.output.append(user_input.strip())
    
    def gather_inputs(self, *coordinates):
        """### Запускает несколько полей ввода одновременно"""
        threads = []
        
        for x, y, prompt in coordinates:
            # Создаем поток для каждого поля ввода
            t = threading.Thread(target=self.input_at, args=(x, y, prompt))
            t.daemon = True
            threads.append(t)
            t.start()
        
        # Ждем завершения всех потоков
        for t in threads:
            t.join()
        
        return self.output

class display:
    def __init__(self):
        templist=[]
        size=terminal_size()
        for lens in range(size[1]): 
            temp={}
            for i in range(size[0]):
                temp[i]=' '
            templist.append(temp)
        self.display=templist
        
    def box(self,px:int, py:int, x:int, y:int, blok='█', filling=False):
        """### create box

        Args:
            px (int): length box
            py (int): height box
            x (int): X Corridate
            y (int): Y Corridate
            blok (str, optional): symbol box. Defaults to '█'.
            filling (bool): заполнен ли квадрат
        """
        
        for xpos in range(x,x+px):
            self.display[y][xpos] = blok
            
        if filling:
            for y in range(y,y+py):
                for xe in range(x,x+px):
                    self.display[y][xe] = blok
        else:
            for y in range(y,y+py):
                self.display[y][x] = blok
                self.display[y][x+px] = blok   
                 
        for xpos in range(x,x+px):
            self.display[py][xpos] = blok
    def cursor(self ,x : int, y : int, symbol='█'):
        try:
            self.display[y]
        except KeyError:
            raise KeyError(f'no the lines end lines {len(self.display)}')
        try:
            for xs in range(x,x+len(symbol)):
                self.display[y][xs] = symbol[xs-x]
        except KeyError:
            raise KeyError(f'There is no such symbol')
    
    def clear_display(self):
        """### clear display"""
        
        self.display={}
        templist=[]
        size=terminal_size()
        for lens in range(size[1]): 
            temp={}
            for i in range(size[0]):
                temp[i]=' '
            templist.append(temp)
        self.display=templist
    
    def echo(self, end='\r') -> str:
        """выводит буфер на экран

        Args:
            end (str, optional): аргумент end. Defaults to '\r'.

        Returns:
            str: содержимое буфера
        """
        
        strings='' # НЕ СТРИНГИ А СТРОКИ
        for i in self.display:
            for st in list(dict(i).keys()):
                strings=strings+i[st]
            strings+='\n'
        print(strings, end=end)
