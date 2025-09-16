from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)


@app.route("/index")
def index():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
                    <div class='spisoklab'><a href="/lab1">Лабораторная работа №1</a></div>
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
                    <div class='spisoklab'><a href="/lab1">Лабораторная работа №1</a></div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>'''

@app.route("/lab1")
def lab1():
    css = url_for('static', filename='123.css')

    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
        <style>
            h2 {
                text-align: center;
                
            }
        </style>
           <body>
                <title>Лабораторная работа 1</title>
                <header>НГТУ, ФБ, WEB-программирование, Лабораторная 1</header>
                    <div>
                        Flask — фреймворк для создания веб-приложений на языке
                        программирования Python, использующий набор инструментов
                        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
                        называемых микрофреймворков — минималистичных каркасов
                        веб-приложений, сознательно предоставляющих лишь самые ба
                        зовые возможности.
                    </div>
                    <a href="/">Список Лабораторных работ</a>
                    <h2>Список роутов:</h2>
                    <div class=menu>
                        <ol class='text'>
                            <li><a href="/index">Главная страница</a></li>
                            <li><a href="/lab1/web">Веб-сервер</a><br>
                            <li><a href="/lab1/author">Автор</a><br>
                            <li><a href="/lab1/image">Изображение</a><br>
                            <li><a href="/lab1/counter">Счетчик</a><br>
                            <li><a href="/lab1/reset_counter">Сброс счетчика</a><br>
                            <li><a href="/lab1/info">Информация</a><br>
                            <li><a href="/lab1/created">Что-то создано</a><br>
                        </ol>
                    </div>
                <footer>Цеунов Мавтей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>'''

@app.route("/lab1/web")
def start():
    return """<!doctype html> 
        <html> 
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/lab1/author">author</a>
           </body> 
        <html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }
     
@app.route("/lab1/author")
def author():
    name = 'Цеунов Матвей Евгеньевич'
    group = 'ФБИ-31'
    faculty = 'ФБ'

    return """<!doctype html>
        <html> 
           <body>
               <p>Студент: """ + name + """</p>
               <p>Группа: """ + group + """</p>
               <p>Факультет: """ + faculty + """</p>
               <a href="/lab1/web">web</a>
          </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="123.png")
    css = url_for("static", filename="lab1.css")
    return '''
        <!doctype html>
        <html>
            <head>
                <link rel="stylesheet" href="''' + css + '''">
            </head>
            <body>
                <h1>Дуб</h1>
                <img src="''' + path + '''">
            </body>
        </html>
        '''

count = 0

@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
    <!doctype html>
        <html>
            <body>
                Сколько раз вы сюда заходили: ''' + str(count) + '''
                <hr>
                Дата и время: ''' + str(time) + ''' <br>
                Запрошенный адрес: ''' + str(url) + ''' <br>
                Ваш IP-адрес: ''' + str(client_ip) + ''' <br>
                <hr>
                <a href="/lab1/reset_counter">Очистить счетчик</a>
            </body>
        </html>'''

@app.route("/lab1/reset_counter")
def reset_counter():
    global count
    count = 0
    return '''
    <!doctype html>
        <html>
            <body>
                Счетчик очищен!
                <hr>
                <a href="/lab1/counter">Вернуться к счетчику</a>
            </body>
        </html>'''

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")


@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html> 
    <body>
        <h1>Созданно успешно</h1>
        <div><i>что-то созданно...</i></div>
    </body>
</html>
''', 201

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404