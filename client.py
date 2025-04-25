import requests
import time
import base64
import tpg
import traceback

# URL сервера
#mein_ulr='http://26.238.36.134:8000/'#URL сервера или же IP

mein_ulr=input('IP server>>')

def binary_to_text(binary_str, encoding='utf-8'):
    #Преобразует двоичную строку обратно в текст
    # Разбиваем строку на части по 8 символов (1 байт)
    bytes_list = [int(binary_str[i:i+8], 2) for i in range(0, len(binary_str), 8)]
    return bytes(bytes_list).decode(encoding)


try:
    a=requests.get(mein_ulr)
except requests.exceptions.InvalidSchema:
    try:
        mein_ulr='http://'+mein_ulr
        a=requests.get(mein_ulr)
        print(a.status_code)
    except requests.exceptions.InvalidSchema:
        print("No connection adapters were found for")
        
url = f'{mein_ulr}/data'
info_url = f'{mein_ulr}/api'
file_list=f'{mein_ulr}/file'

def ping(ping_url)->int:
    start_time = time.time()
    try:
        k=requests.get(ping_url)
        s=k.status_code
        if s== 200:
            pass
        else:
            return s
    except requests.exceptions.InvalidURL:return f"Invalid url >> {ping_url}"
    except requests.exceptions.ConnectionError: return "not connect"
    response=time.time() - start_time
#    print('ping',response)
    return response

print(f"ping>>>{ping(url)}")
try:
    # POST-запрос с JSON
    info_data = {'key': 'value'}
    info = eval(binary_to_text(requests.post(info_url, json=info_data).json()))
    # Вывод POST-ответа
    print('info:', info)
    #проверка сервера на коректность
    if info['key']>10 or info['key']<0:
        print('error server key conecting')
        for i in range(5):
            info = binary_to_text(requests.post(info_url, json=info_data).json())
            time.sleep(1)
            if info['key']>10 or info['key']<0:
                print('error server key conecting')
                if i >=5:
                    exit('error server key conecting')
            else:
                break
    
    # GET-запрос с параметрами
    params = {'key': 'value'}

    response = requests.get(file_list, params=params)
    files = response.json()  # Получаем данные из GET-запроса

    file_download =tpg.listgr(files,title=info['message'])

    params = {'file': file_download}
    bute = requests.get(url, params=params).json()
    if file_download in files:  # Проверяем, существует ли файл
        # Запись содержимого файла
        file_content = base64.b64decode(bute['data'])
        with open(file_download, 'wb') as f:
            f.write(file_content)
        print(f"File {bute['message']} downloaded successfully.")
    else:
        print('key data not found')
except Exception as e:
    print('error>\n'+traceback.format_exc()+'\n')
    input('press enter to exit')

