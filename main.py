from jinja2 import Environment, FileSystemLoader, select_autoescape
from sanic import Sanic, response, json, redirect, html, file, text
import subprocess
from threading import Thread
from database import *
from sanic_session import Session
from datetime import datetime

app = Sanic("HackathonCampus") #Инициализировали Sanic

env = Environment( #Инициализировали Jinja2
    loader=FileSystemLoader('templates'),  # Указали путь к шаблонам для Jinja2
    autoescape=select_autoescape(['html', 'xml']) # Указали типы файлы
)

app.static("/static/", "./static/") # Маршрут на папку со статичными файлами

Session(app)

@app.get('/') # Маршрут на первоначальную страницу
async def index(request):
    user = request.ctx.session.get('user_id')
    data = {}
    template = env.get_template('index.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.post('/like/post')
async def like_post(request):
    userid = request.ctx.session.get('user_id')
    postid = request.json.get('postid')
    if not userid: return text("Unauthorized", status=401)
    if not postid: return text("Bad request", status=400)
    
    return json({'status':'OK', 'liked':Database.likePost(userid, postid)}, status=200)

@app.get('/posts')
async def get_posts(request):
    user_id = request.ctx.session.get('user_id')
    if not user_id: 
        return json({'posts':Database.getAllPosts()}, status=200)
    return json({'posts':Database.getPostsForUser(user_id)}, status=200)

@app.get('/about')
async def about(request):
    data = {}
    template = env.get_template('about.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.route('/servevideo/<filename:str>')
async def serve_video(request, filename):
    video_path = './static/video/' + filename
    # Открываем файл видео
    with open(video_path, 'rb') as video_file:
        video_data = video_file.read()

    headers = {'Accept-Ranges': 'bytes'}
    content_range = request.headers.get('Range')

    if content_range:
        # Разбираем значение Range заголовка
        start, end = content_range.replace('bytes=', '').split('-')
        start = int(start)
        end = int(end) if end else len(video_data) - 1

        # Определяем длину контента и формируем заголовок Content-Range
        content_length = end - start + 1
        headers['Content-Range'] = f'bytes {start}-{end}/{len(video_data)}'
        
        # Вырезаем запрошенный диапазон данных из файла
        video_chunk = video_data[start:end+1]
        return response.raw(video_chunk, headers=headers, status=206)

    # Если Range не указан, отправляем весь файл
    return await response.file_stream(video_path, headers=headers)

@app.route('/images/<image:str>')
async def serve_image(request, image):
    return response.file('./static/images/' + image)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)