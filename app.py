from flask import Flask, url_for, request, redirect, abort, render_template, session
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager
import os 
from os import path
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
import datetime

app = Flask(__name__)


login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


if app.config['DB_TYPE'] == 'postgres':
    db_name = 'tseunov_matvey_orm'
    db_user = 'tseunov_matvey_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = '5432'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'

else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "tseunov_matvey_orm")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)



app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)


@app.route("/index")
def index():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
                    <div><a href="/lab1">Лабораторная работа №1</a></div>
                    <div><a href="/lab2">Лабораторная работа №2</a></div>
                    <div><a href="/lab3">Лабораторная работа №3</a></div>
                    <div><a href="/lab4">Лабораторная работа №4</a></div>
                    <div><a href="/lab5">Лабораторная работа №5</a></div>
                    <div><a href="/lab6">Лабораторная работа №6</a></div>
                    <div><a href="/lab7">Лабораторная работа №7</a></div>
                    <div><a href="/lab8">Лабораторная работа №8</a></div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>'''

@app.route("/")
def a():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
                    <div><a href="/lab1">Лабораторная работа №1</a></div>
                    <div><a href="/lab2">Лабораторная работа №2</a></div>
                    <div><a href="/lab3">Лабораторная работа №3</a></div>
                    <div><a href="/lab4">Лабораторная работа №4</a></div>
                    <div><a href="/lab5">Лабораторная работа №5</a></div>
                    <div><a href="/lab6">Лабораторная работа №6</a></div>
                    <div><a href="/lab7">Лабораторная работа №7</a></div>
                    <div><a href="/lab8">Лабораторная работа №8</a></div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>'''


@app.errorhandler(500)
def not_found2(err):
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body class='bodyerror'>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <div class='error1'>Внутренняя ошибка сервера!<br>Сервер столкнулся с внутренней ошибкой и не смог выполнить ваш запрос. Сервер перегружен, либо в приложении произошла ошибка.</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 500




@app.errorhandler(404)
def not_found(err):
    return redirect("/lab1/404")

visit_log = []

@app.route("/lab1/404")
def not_found():
    global visit_log
    

    client_ip = request.remote_addr
    access_time = datetime.datetime.today()
    requested_url = request.url
    

    visit_log.append({
        'ip': client_ip,
        'time': access_time,
        'url': requested_url
    })
    
    css = url_for('static', filename='123.css')
    path = url_for("static", filename="lab1/2.jpg")
    

    html_content = f'''<!doctype html>
        <html> 
        <link rel="stylesheet" href="{css}">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы - Ошибка 404</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                
                <div><strong>Ошибка 404</strong></div>
                <div>Код ответа на статус ошибки 404. Ошибка 404 — это код ответа HTTP. Он означает, что браузер не нашёл на сервере URL — адрес ресурса в интернете, который пользователь ввёл в адресную строку.</div>
                
                <hr>
                <div><strong>Информация о текущем посещении:</strong></div>
                <div>Ваш IP-адрес: {client_ip}</div>
                <div>Дата и время доступа: {access_time}</div>
                <div>Запрошенный адрес: {requested_url}</div>
                
                <div style="margin: 20px 0;">
                    <a href="{url_for('index')}">Вернуться на главную страницу</a>
                </div>
                
                <img src="{path}">
                
                <hr>
                <div><strong>Лог посещений страницы 404:</strong></div>
                <div style="max-height: 200px; overflow-y: auto; border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
    '''
    

    for entry in reversed(visit_log):
        html_content += f'''
                    <div style="margin: 5px 0; padding: 5px; background: #f0f0f0;">
                        IP: {entry['ip']} | 
                        Время: {entry['time']} | 
                        URL: {entry['url']}
                    </div>
        '''
    
    html_content += f'''
                </div>
                
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>'''
    
    return html_content, 404










