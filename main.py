import time
import os
import requests
import base64
import random
import json
import traceback


from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
import socket


settings=''
try:
    with open("settings.json", "r") as json_settings:
        settings= json.load(json_settings)
    print(settings)
    port=int(settings['port'])
    dictoru=os.path.join(os.getcwd(),settings["dictoru"])
    message=str(settings["message"])
    host_file_On_the_site=bool(settings['host_file_On_the_site'])
except Exception as e: 
    print('error import settngs')
    print(f"error>> {e} \n{traceback.format_exc()}")
    port=8000#порт 
    dictoru=os.path.join(os.getcwd(),'file')#путь к папке с файлами
    message='hello'
    host_file_On_the_site=True# возможность качать файлы с сайта без клиента 
    settings={"dictoru":"file"}

data={}
if os.path.isdir(dictoru) != True:
    print('\33[31m'+f'error no {dictoru}')
     
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
            if s == 200:
                pass
            else:
                return s
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
print(f'server IP > http://{get_local_ip()}:{port}')

@app.post('/api')
def handle_get():
    # key нужен для проверки на коректность сервера
    return {'ip':get_local_ip(),'port':port,'key':random.randint(0,10),'message':message}

# Обработка GET-запроса
@app.get('/file')
async def handle_get():
    try:
        file_list = os.listdir(dictoru)
        file_sizes = {f: os.path.getsize(os.path.join(dictoru, f)) for f in file_list}
        return {"file_list": file_sizes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount('/'+settings["dictoru"], StaticFiles(directory=settings["dictoru"]), name="file_dir")
@app.get('/', response_class=HTMLResponse)
async def handle_get():
    if host_file_On_the_site:
        file_no_the_site=''
        description='no description'
        try:
            with open("description_file.json", "r") as json_settings:
                description_file=json.load(json_settings)
        except FileNotFoundError:
            description_file=None
        for i in os.listdir(dictoru):
            if description_file is not None:
                try:
                    description=f'<h3>{description_file[i]}</h3>'
                except KeyError:
                    description='no description'
            file_no_the_site+=f'<a href="{settings["dictoru"]}/{i}" download>Download {i}</a><br>\n{description}<br>'
        return f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <title>server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
            </head>
            <body>
                <h1>connect</h1>
                {file_no_the_site}


                <a href="/upload">upload file</a>
            </body>
        </html>
    """
    else:    
        return f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <title>server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
            </head>
            <body>
                <h1>connect </h1>
                <h2>для скачивания файлов нужен клиент</h2>

            </body>
        </html>
    """
    
@app.get("/upload", response_class=HTMLResponse)
async def main():
    content = """
    <html>
        <head>
            <meta charset="UTF-8">
            <title>File Upload</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
        </head>
        <body>
            <h1>Upload a File</h1>
            <form action="/uploadfile/" enctype="multipart/form-data" method="post">
                <input name="file" type="file">
                <input type="submit">
            </form>
        </body>
    </html>
    """
    return content

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(dictoru , file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    
    
def read_data(file):
    file_path = os.path.join(dictoru, file)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                yield base64.b64encode(chunk).decode('utf-8')

@app.get('/data')
async def handle_get(file: str):
    return StreamingResponse(
        read_data(file),
        media_type="application/octet-stream",
        headers={
            "Transfer-Encoding": "chunked"

        }
    )
    # {'message': file,"Content-Length": os.path.getsize(file_path) + 1}
# Запуск сервера
if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(app, host='0.0.0.0', port=port)
