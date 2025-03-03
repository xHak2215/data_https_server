import requests
import time
import base64

# URL сервера
mein_ulr='http://localhost:8000/'#URL сервера или же IP

url = f'{mein_ulr}data'
info_url = f'{mein_ulr}'

def ping(ping_url)->int:
    start_time = time.time()
    try:
        try:
            k=requests.get(ping_url)
            s=k.status_code
            if s== 200:
                pass
            else:
                return s
        except requests.exceptions.InvalidURL:
            return f"Invalid url >> {ping_url}"
    except requests.exceptions.ConnectionError: return "not connect"
    response=time.time() - start_time
#    print('ping',response)
    return response

print(f"ping>>>{ping(url)}")
# POST-запрос с JSON
info_data = {'key': 'value'}
info = requests.post(info_url, json=info_data)
# Вывод POST-ответа
print('POST response:', info.json())
# GET-запрос с параметрами
params = {'key': 'value'}
response = requests.get(url, params=params)

# Вывод результатов
data = response.json()  # Получаем данные из GET-запроса

# Обработка данных
if 'data' in data:  # Проверяем, есть ли ключ 'data' в ответе
    files = data['data']  # Получаем словарь с файлами
    print("Available files:", list(files.keys()))

    # Запрос имени файла для загрузки
    file_download = input('file download >> ')
    if file_download in files:  # Проверяем, существует ли файл
        # Запись содержимого файла
        file_content = base64.b64decode(data['data'][file_download])
        with open(file_download, 'wb') as f:
            f.write(file_content)
        print(f"File '{file_download}' downloaded successfully.")
    else:
        print(f"File '{file_download}' not found.") 
else:
    print("No files available in the response.")

