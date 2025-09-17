import requests
import tpg

import time
import base64
import traceback
import os
import bz2
import json


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
            return 'code '+str(s)
    except requests.exceptions.InvalidURL:return f"Invalid url >> {ping_url}"
    except requests.exceptions.ConnectionError: return "not connect"
    response=time.time() - start_time
#    print('ping',response)
    return response

print(f"ping>>>{ping(url)}")
# POST-запрос с JSON
info_data = {'key': 'value'}
info = requests.post(info_url, json=info_data).json()
# Вывод POST-ответа
print('info:', info ,)
#проверка сервера на коректность
if int(info['key'])>10 or int(info['key'])<0:
    print('error server key connecting')
    for i in range(5):
        info = requests.post(info_url, json=info_data).json()
        time.sleep(1)
        if info['key']>10 or info['key']<0:
            print('error server key connecting')
            if i >=5:
                exit('error server key connecting')
        else:
            break

list_response = requests.get(file_list, params={'key': 'value'})
list_response.raise_for_status()  # Проверяем HTTP-ошибки
data = list_response.json()
files=data["file_list"]
file_list=list(files.keys())

# 2. Выбираем файл для загрузки
file_download = tpg.listgr(file_list, title=info['message'])

if file_download not in file_list:
    raise ValueError("Файл не найден в списке")

# 3. Загружаем файл с прогресс-баром
SAFE_DIR = "downloads"
os.makedirs(SAFE_DIR, exist_ok=True)
file_path = os.path.join(SAFE_DIR, file_download)

time.sleep(2)
token=1#input("input token>>")

get_url=f"{url}/{file_download}/{token}"
download_response = requests.get(get_url, stream=True)
#download_response.raise_for_status()

#total_size = int(download_response.headers.get('Content-Length', 1))
total_size=files[file_download]
total_bytes=0
num=0
while os.path.isfile(file_path):
    num=+1
    file_path=f"({num}){file_path}"

datas=''
timer=time.time()
for chunk in download_response.iter_content(chunk_size=8192):
    if chunk:
        total_bytes += len(chunk)
        percent = round(100/(total_size/total_bytes) ,2)
        bar=int(round(percent))
        if bar >= 100:
            progress_bar=f'[    successfully    ] {round(time.time()-timer,1)}s. '
        else:
            progress_bar=f"[{'#'*bar}{' '*(20-bar)}]"
        tpg.clear()
        print(f"{progress_bar}{percent:.1f}% ({total_bytes} / {total_size} byte) ")
        datas=datas+str(chunk.decode())
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(chunk.decode()))
print(f"Файл {file_download} успешно загружен.")

'''
if "error" in list(json.loads(datas)).keys():
    if json.loads(datas)["error"] == None:
        tpg.clear()

        print(f"Файл {file_download} успешно загружен.")
    else:
        #tpg.clear()
        print(tpg.color(f"server response error>{json.loads(datas)["error"]}",'red'))
else:
    #tpg.clear()
    print(tpg.color(f"server response error> {str(json.loads(datas))}",'red'))
'''
    






