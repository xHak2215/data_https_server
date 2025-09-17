
<details>
  <summary>languages</summary>
    <li>
      <ul>
      <li><a href="https://github.com/xHak2215/tpg/blob/main/doc/eng_README.md">English</a></li>
      </ul>
    </li>
</details>

TPG - Terminal Python Graphics (UI)
A small library for creating graphical interfaces

Library features include:

- Lists
- Simplified color handling (ANSI)
- Console cursor control
- Yes/No selection menu
- Settings with JSON support

Examples and basic functionality:
Control: Move cursor up/down with arrows, select with Enter

---

### listgr:

```python
import tpg # import lib
out_point = listgr(['point1','point2','point3'])
print(out_point)
```

Arguments:

- kastor - parameter for the cursor symbol before selected item (default '>')
- title - text above the list
- style - default style 'standard', other option 'scob'
Control: Move cursor up/down with arrows, change with Enter, exit with Esc
- ansi - ability to use ANSI escape sequences in the menu, just pass the ANSI sequence (recommended to use the `color` function described below)

How it looks:

![hippo](doc/list_test.gif)

### settings:

```python
import tpg # import lib

out = settings({'point1':True,'point2':False}) # change dict
print(out) # print updated dict from json file

out = settings({}, jsonf='test_json.json') # read and write json file
print(out) # print updated dict
```

![hippo](doc/settings_ui_test.gif)

In the first case, a dictionary is passed to the function. It can have any keys and any number of them, but values must be True or False. The function returns the updated dictionary modified by the user.

In the second case, the dictionary is loaded from a JSON file specified in the `jsonf` argument. After user modifications, the JSON file will be updated and the function will return the modified dictionary from the JSON.

### yes_or_no:

```python
import tpg # import lib

if yes_or_no('yes or no'): # yes - True, no - False
    print("Pressed yes")
else:
    print('Pressed no')
```

Takes one argument for the prompt text at the top.
Returns True if 'yes' is selected and False if 'no' is selected.

### color:

```python
import tpg 

# color color/text_color, style, background/background_color
print(color('red','standard','yellow') + 'green text, yellow background') 
print(color('clear')) # clear colors
print('text')
```

Available colors:

- black
- red
- green
- yellow
- blue
- violet
- turquoise
- white
Can be used for both text and background colors

## display class:

Functions:

- cursor
- echo

Examples:

Text output by coordinates:

```python
import tpg

display = tpg.display()

display.cursor(5,5)

display.echo()
```
