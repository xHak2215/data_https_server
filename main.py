import time
import os
import requests
import base64
import random
import json
import traceback
import socket


from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


try:
    with open("settings.json", "r") as json_settings:
        settings = json.load(json_settings)
    port = int(settings['port'])
    directory = os.path.join(os.getcwd(),settings["directory"])
    message = str(settings["message"])
    host_file_On_the_site = bool(settings['host_file_on_the_site'])

except Exception as e: 
    print("error import settings")
    print(f"error>> {e} \n{traceback.format_exc()}")
    port = 8000
    directory = os.path.join(os.getcwd(),'file')#путь к папке с файлами
    message = "hello"
    host_file_On_the_site = True# возможность качать файлы с сайта без клиента 
    settings = None

data={}
if os.path.isdir(directory) != True:
    print(f"\33[31merror no {directory} \33[0m")
     
# uvicorn main:app --reload
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Не важно, что эта IP не существует, нам нужен только сокет
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def text_to_binary(text, encoding='utf-8'):
    #Преобразует текст в двоичную строку (последовательность '0' и '1')
    binary_data = ''.join(format(byte, '08b') for byte in text.encode(encoding))
    return binary_data

def ping(ping_url)->float|str:
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
    
print(f"host directory>> {directory}")
print(f"server IP > http://{get_local_ip()}:{port}")

mount_dir = os.path.join(os.getcwd(), "mount_dir")
app.mount("/mount_dir", StaticFiles(directory = mount_dir), name = "mount_dir")
app.mount("/files", StaticFiles(directory = directory), name = "files")

@app.post('/api')
def api():
    return {'ip':get_local_ip(), 'port':port, 'message':message}

@app.get('/file')
async def get_file():
    try:
        file_list = os.listdir(directory)
        file_sizes = {f: os.path.getsize(os.path.join(directory, f)) for f in file_list}
        return {"file_list": file_sizes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
        
        file_no_the_site=file_no_the_site+f'<a href="/cd?dir=..">←</a> <br><br>'

        for i in os.listdir(directory):
            if description_file is not None:
                try:
                    description=f"<h3>{description_file[i]}</h3>"
                except KeyError:
                    description="no description"
            
            button_buffer = ""
            
            if os.path.isfile(os.path.join(directory, i)):
                if i[0] != "." and "." in i:
                    print(i)
                    rashirenie = i.rsplit(".", 1)[1]
                    if rashirenie in ["mp4", "m4v", "mkv", "mov", "avi", "webm", "flv", "ts", "m2ts", "mts", "3gp", "3g2", "wmv", "asf", "ogv", "mxf", "gif", "dv", "rm", "rmvb", "f4v"]:
                        button_buffer = f'<div class="player_button"> <a href="/video_play?file={i}" class="button-like">play</a> </div>'
                    elif rashirenie in ["aac", "mp3", "opus", "ogg", "oga", "wav", "flac", "alac", "ac3", "eac3"]:
                        button_buffer = f'<div class="player_button"> <a href="/audio_play?file={i}" class="button-like">play</a> </div>'
                file_no_the_site=file_no_the_site+f'<a href="files/{i}" download>Download {i[:150]}</a> {button_buffer} <br>\n <p>{description}</p> <br>'

            elif os.path.isdir(os.path.join(directory, i)):
                file_no_the_site=file_no_the_site+f'<a href="/cd?dir={i}">→ {i[:150]}</a> <br>\n <p>{description}</p> <br>'

        content=f"""
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title>server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0">
                <link rel="stylesheet" href="/mount_dir/front/style.css">
                <link rel=”icon” href="/mount_dir/favicon.ico" type=”image/x-icon”>
            </head>
            <body>
                <hr size="6" color="gray">
                <h2>files:</h2>
                <br>

                {file_no_the_site}
                <hr size="5" color="gray">
                <h3> <a href="/upload">upload file</a> </h3>
            </body>
        </html>
        """
        return content
    else:
        response.status_code = 403    
        return f"""
        <html>
            <head>
                <meta charset="UTF-8">
                <title>server</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
                <link rel="stylesheet" href="/mount_dir/front/style.css">
                <link rel=”icon” href="/mount_dir/favicon.ico" type=”image/x-icon”>
            </head>
            <body>
                <h2>для скачивания файлов нужен клиент</h2>
            </body>
        </html>
    """
    
@app.get("/upload", response_class=HTMLResponse)
async def main():
    content = f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <title>File Upload</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
            <link rel="stylesheet" href="/mount_dir/front/style.css">
            <link rel=”icon” href="/mount_dir/favicon.ico" type=”image/x-icon”>
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

@app.get("/video_play", response_class=HTMLResponse)
async def video_player(file:str):
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <title>video player</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
            <link rel="stylesheet" href="/mount_dir/front/style.css">
            <link rel=”icon” href="/mount_dir/favicon.ico" type=”image/x-icon”>
        </head>
    <body>
    <video src="/files/{file}" controls></video>

    </body>
    </html>
    """

@app.get("/audio_play", response_class=HTMLResponse)
async def audio_player(file:str):
    return f"""
    <html>
        <head>
            <meta charset="UTF-8">
            <title>audio player</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=2.0"> 
            <link rel="stylesheet" href="/mount_dir/front/style.css">
            <link rel=”icon” href="/mount_dir/favicon.ico" type=”image/x-icon”>
        </head>
    <body>
    <audio controls src="/files/{file}"></audio>

    </body>
    </html>
    """

@app.get("/cd")
async def cd_in_dir(dir:str):
    global directory
    if dir == "..":
        directory = directory.rsplit("/", 1)[0]

    if dir in os.listdir(directory):
        directory = os.path.join(directory, dir) 
    return RedirectResponse("/")

@app.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(directory, file.filename)
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}
    
    
def read_data(file):
    file_path = os.path.join(directory, file)
    if os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                yield base64.b64encode(chunk).decode('utf-8')

@app.get('/data')
async def stream_data(file: str):
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
    uvicorn.run(app, host=get_local_ip(), port=port)
