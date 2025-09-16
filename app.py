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



@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404

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

@app.route("/web")
def start():
    return """<!doctype html> 
        <html> 
           <body>
               <h1>web-сервер на flask</h1>
               <a href="/author">author</a>
           </body> 
        <html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }
     
@app.route("/author")
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
               <a href="/web">web</a>
          </body>
        </html>"""

@app.route("/image")
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

@app.route("/counter")
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
                <a href="/reset_counter">Очистить счетчик</a>
            </body>
        </html>'''

@app.route("/reset_counter")
def reset_counter():
    global count
    count = 0
    return '''
    <!doctype html>
        <html>
            <body>
                Счетчик очищен!
                <hr>
                <a href="/counter">Вернуться к счетчику</a>
            </body>
        </html>'''

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/info")
def info():
    return redirect("/author")


@app.route("/created")
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
