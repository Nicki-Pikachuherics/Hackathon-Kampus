from jinja2 import Environment, FileSystemLoader, select_autoescape
from sanic import Sanic, response, json, redirect, html, file, text
import subprocess
from threading import Thread
from database import *
from sanic_session import Session
from datetime import datetime
import telebot

app = Sanic("HackathonCampus") #Инициализировали Sanic

env = Environment( #Инициализировали Jinja2
    loader=FileSystemLoader('templates'),  # Указали путь к шаблонам для Jinja2
    autoescape=select_autoescape(['html', 'xml']) # Указали типы файлы
)

app.static("/static/", "./static/") # Маршрут на папку со статичными файлами

Session(app)

@app.route('/') # Маршрут на первоначальную страницу
async def index(request):
    data = {}
    template = env.get_template('index.html') #Получили шаблон
    return response.html(template.render(data=data))

@app.route('/images/<image>')
async def serve_image(request, image):
    return response.file('./static/images/' + image)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)