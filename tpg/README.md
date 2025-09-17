
</details>
  <summary>languages</summary>
    <li>
      <ul>
      <li><a href="https://github.com/xHak2215/tpg/blob/main/doc/eng_README.md">English</a></li>
      </ul>
    </li>
</details>

TPG - terminal python graphics (UI)
небольшая библиотека для создания графических интерфейсов

в функционал библиотеки входят :

- списки
- упрощеная работа с цветами (ANSI)
- упровление курсором кансоли
- меню выбора (да/нет)
- настройки с потдержкой json

примеры и базовый функционал
упровление: перемещение курсора в верх в низ стрелки, выбор - enter

---

### listgr:

```python
import tpg #inport lib
out_point=listgr(['point1','point2','point3'])
print(out_point)
```

аргументы:
kastor - параметре отвечающий за курсор стоящий перед выбранным пунктом (по умолчанию '>')

title - текст над списком

style - стиль по умолчанию 'standart' другие 'scob'

управление: перемещение курсора в верх в низ стрелки,изменение - enter,заверщение - esc

ansi - возможность использовать ANSI escape sequences в меню достаточно лишь передать ANSI последовательность советую использовать функцию `color` описанную ниже

как это выгледит

![hippo](doc/list_test.gif)

### settings:

```python
import tpg #inport lib

out=settings({'point1':true,'point2':false}) # change dict
print(out) # print new dict from json file

out=settings({},jsonf='test_json.json')# read and write json file 

print(out) # print new dict 

```

![hippo](doc/settings_ui_test.gif)

в 1 случае в функцию был передан словарь он может быть с любыми ключами и их количеством но  
значения должно быть true или false функция вернет обновлённый словарь измененый пользователем

во 2 случае словарь извлекается из json файла его име указывается в аргументе `jsonf` после пользовательских изменений json файл будет изменен а функция вернёт словарь с изменёнными данными из json

### yes_or_no:

```python
import tpg #inport libs

if yes_or_no('yes or no'): # yes - True no -false 
    print("press yes") 
else:
    print('press no')  
```

передаеться 1 аргумент отвечающий за натрись в верху
возврощаеться True если выбрано yes и false если no

### color:

```python
from tpg import * #inport libs

# color color/цвет,stule/стиль,beggraubd/задний фон
print(color("green text,yelou begraund",'red','standart','yelou')) 
print('text') 
```

есть цвета :

- blak
- red
- green
- yelou
- blue
- violet
- beruza
- white
подходят как для заднего фона так и для цвета текста

## класс display:

функции:

- cursor
- echo
- box

примеры:

вывод текста по кординатам:

```python
import tpg

displu=tpg.display()

displu.cursor(5,5)

displu.echo()

```

вывод 2 прямоугольников (квадратов с задаными свойствами) где в одном находиться текст а другой залит

```python
import tpg

displu=tpg.display()

displu.box(15, 11, 1, 1,blok='@')

displu.box(15, 11, 22, 1, filling=True)

displu.cursor(3,3 ,symbol='hi')

displu.echo(end='\n')

```

