import requests
import tpg

import time
import base64
import traceback
import os
import bz2


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

    list_response = requests.get(file_list, params={'key': 'value'})
    list_response.raise_for_status()  # Проверяем HTTP-ошибки
    files = list_response.json()
    
    if not isinstance(files, list):
        raise ValueError("Сервер вернул не список файлов")

    # 2. Выбираем файл для загрузки
    file_download = tpg.listgr(files, title=info['message'])
    if file_download not in files:
        raise ValueError("Файл не найден в списке")

    # 3. Загружаем файл с прогресс-баром
    SAFE_DIR = "downloads"
    os.makedirs(SAFE_DIR, exist_ok=True)
    file_path = os.path.join(SAFE_DIR, file_download)

    download_response = requests.get(url, params={'file': file_download}, stream=True)
    download_response.raise_for_status()

    total_size = int(download_response.headers.get('content-length', 0))
    
    total_bytes=0
    with open(file_path, 'wb') as f:
        timer=time.time()
        for chunk in download_response.iter_content(chunk_size=8192):
            if chunk:
                total_bytes += len(chunk)
                percent = (total_bytes / total_size) * 100 if total_size > 0 else 0
                i = round(20 * (percent / 100))
                if percent >= 100:
                   progress_bar=f'[    successfully    ] {round(timer-time.time()/1000) if timer-time.time() < 1000 else 1 }s.'
                else:
                    progress_bar=f"[{'#'*i}{' '*(20-i)}]"
                print(f"{progress_bar}{percent:.1f}% ({total_bytes} / {total_size} байт)")
                # Распаковка
                f.write(base64.b64decode(chunk))
                tpg.clear()
    
    print(f"Файл {file_download} успешно загружен.")

except Exception as e:
    print(f"Ошибка: {e}")
    print(traceback.format_exc())
    input('Нажмите Enter для выхода...')

