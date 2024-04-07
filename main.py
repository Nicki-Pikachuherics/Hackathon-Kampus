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
    user = Database.getUserById(user)
    data = {}
    if user:
        data['user'] = user
    template = env.get_template('index.html') #Получили шаблон
    return response.html(template.render(data=data))
@app.get('/login')
async def login(request):
    data = {}
    template = env.get_template('login.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.post('/login')
async def login_input(request):
    username = request.form.get('username')
    password = request.form.get('password')
    logged_in = Database.loginUser(username, password)
    if logged_in:
        request.ctx.session['user_id'] = logged_in['id']
        return redirect('/')
    else:
        return redirect('/login')

@app.get('/profile')
async def profile(request):
    user = request.ctx.session.get('user_id')
    user = Database.getUserById(user)
    data = {}
    if user:
        data['user'] = user
    else: return redirect('/')
    template = env.get_template('profile.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.post('/update_user_info')
async def update_user_info(request):
    user = request.ctx.session.get('user_id')
    login = request.form.get('login')
    password = request.form.get('password')
    Database.updateUserInfo(user, login, password)
    return redirect('/profile')

@app.get('/event/<eventid:int>') # Маршрут на страницу события
async def event(request, eventid):
    user = request.ctx.session.get('user_id')
    event = Database.getEventById(eventid)
    data = {}
    data['event'] = event
    template = env.get_template('event.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.get('/post/comments')
async def get_comments(request):
    user = request.ctx.session.get('user_id')
    postid = request.args.get('postid')
    post = Database.getPostById(postid)
    #TODO: Проверка на то, существует ли пост и пользователь имеет права просматривать его
    commentscount = request.args.get('count')
    if not commentscount: commentscount = 3
    comments = Database.getPostComments(postid)
    return json({'comments':comments[:int(commentscount)], 'maxcount':len(comments)}, status=200)

@app.get('/post')
async def get_post(request):
    user = request.ctx.session.get('user_id')
    postid = request.args.get('postid')
    if not postid: return text("Bad request", status=400)
    post = Database.getPostById(postid)
    #TODO: Проверка на то, существует ли пост и пользователь имеет права просматривать его
    data = {}
    data['post'] = post
    template = env.get_template('post.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.post('/comment/post')
async def comment_post(request):
    userid = request.ctx.session.get('user_id')
    postid = request.json.get('postid')
    text = request.json.get('text')
    if not userid: return text("Unauthorized", status=401)
    if not postid: return text("Bad request", status=400)
    if not text: return text("Bad request", status=400)
    Database.CommentPost(userid, postid, text)
    return json({'status':'OK'}, status=200)

@app.post('/like/post')
async def like_post(request):
    userid = request.ctx.session.get('user_id')
    postid = request.json.get('postid')
    if not userid: return text("Unauthorized", status=401)
    if not postid: return text("Bad request", status=400)
    
    return json({'status':'OK', 'liked':Database.likePost(userid, postid)}, status=200)

@app.post('/post/create')
async def create_post(request):
    userid = request.ctx.session.get('user_id')
    if not userid: return text("Unauthorized", status=401)
    data = request.json
    if not data: return text("Bad request", status=400)
    Database.createPost(userid, data)

@app.get('/university/<universityname:str>')
async def university(request, universityname):
    university = Database.getUniversityByName(universityname)
    template = env.get_template('university.html')
    data = {}
    data['university'] = university
    return response.html(template.render(data=data))

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
    with open(video_path, 'rb') as video_file:
        video_data = video_file.read()
    headers = {'Accept-Ranges': 'bytes'}
    content_range = request.headers.get('Range')
    if content_range:
        start, end = content_range.replace('bytes=', '').split('-')
        start = int(start)
        end = int(end) if end else len(video_data) - 1
        headers['Content-Range'] = f'bytes {start}-{end}/{len(video_data)}'
        video_chunk = video_data[start:end+1]
        return response.raw(video_chunk, headers=headers, status=206)
    return await response.file_stream(video_path, headers=headers)

@app.route('/images/<image:str>')
async def serve_image(request, image):
    return response.file('./static/images/' + image)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)