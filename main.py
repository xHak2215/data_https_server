from fastapi import FastAPI, Request
from pydantic import BaseModel
import socket
import requests
import time
import os
import base64

port=8000#порт 
dictoru='file'#нуть к папке с файлами
data={}

# uvicorn main:app --reload
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def ping(ping_url)->int:
    start_time = time.time()
    try:
        try:
            k=requests.get(ping_url)
            s=k.status_code
            if s== 200:
                pass
            else:
                return "not"
        except requests.exceptions.InvalidURL:
            return f"Invalid url >> {ping_url}"
    except requests.exceptions.ConnectionError: return "not connect"
    response=time.time() - start_time
#    print('ping',response)
    return response

app = FastAPI()
# Модель данных для POST-запроса
class Item(BaseModel):
    key: str

# Обработка GET-запроса
@app.post('/')
def handle_get():
    return {'info': f"ip:{get_local_ip()},port:{port}"}


@app.get('/data')
def handle_get():
    for file_data in os.listdir(dictoru):  # Используем абсолютный путь
        file_path = os.path.join(dictoru, file_data)
        if os.path.isfile(file_path):  # Проверяем, что это файл
            with open(file_path, 'rb') as file:  # Читаем файл как текст
                data[file_data] = base64.b64encode(file.read()).decode('utf-8')
    return {'message': file_data, 'data': data}
# Запуск сервера
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=get_local_ip(), port=port)