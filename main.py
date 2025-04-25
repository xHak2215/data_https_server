from fastapi import FastAPI, Request
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import socket
import requests
import time
import os
import base64
import random

port=8000#порт 
dictoru=os.getcwd()+'\\file'#путь к папке с файлами
data={}
message='hello'

# uvicorn main:app --reload
def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def text_to_binary(text, encoding='utf-8'):
    #Преобразует текст в двоичную строку (последовательность '0' и '1')
    binary_data = ''.join(format(byte, '08b') for byte in text.encode(encoding))
    return binary_data

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
    
print('host direktoru>>',dictoru)
print(f'server IP >http://{get_local_ip()}:{port}')

@app.post('/api')
def handle_get():
    # key нужен для проверки на коректность сервера
    return text_to_binary(str({'ip':get_local_ip(),'port':port,'key':random.randint(0,10),'message':message}))

# Обработка GET-запроса
@app.get('/file')
def handle_get():
    return list(os.listdir(dictoru))
@app.get('/', response_class=HTMLResponse)
async def handle_get():
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <title>server</title>
        </head>
        <body>
            <h1>conect</h1>
            <h2>для скачивания файлов нужен клиент скачайте его тут:</h2>
            <h2>To download files, you need a client download it here:</h2>
            <a href="http://{get_local_ip()}:{port}/client" a>download</a>
        </body>
    </html>

    """
app.mount("/bin", StaticFiles(directory="bin"), name="bin")
@app.get("/client", response_class=HTMLResponse)
async def read_root():
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <title>client download</title>
        </head>
        <body>
            <h1>client download</h1>
            <h2>для запуска нужен python и библиотека requests</h2>
            <h2>You need Python and the REQUESTS library for launch</h2>
            
            <a href="bin/local_data_client.zip" download>Download code</a><br>
            <a href="bin/client.exe" download>Download exe file for Windows</a>
        </body>
    </html>
    """
@app.get('/data')
def handle_get(file:str):
    file_path = os.path.join(dictoru, file)
    if os.path.isfile(file_path):  # Проверяем, что это файл
        with open(file_path, 'rb') as file:  # Читаем файл как bin
            data = base64.b64encode(file.read()).decode('utf-8')
    return {'message': file, 'data': data}
# Запуск сервера
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=port)
