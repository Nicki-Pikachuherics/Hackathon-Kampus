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
    print(user)
    request.ctx.session['user_id'] = 123
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

@app.route('/images/<image>')
async def serve_image(request, image):
    return response.file('./static/images/' + image)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)