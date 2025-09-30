from flask import Flask, url_for, request, redirect, abort, render_template
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
                    <div><a href="/lab1">Лабораторная работа №1</a></div>
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
                            <li><a href="/lab1/error1">Список ошибок</a><br>
                        </ol>
                    </div>
                <footer>Цеунов Мавтей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>'''

@app.route("/lab1/error1")
def error1():
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
                    <a href="/">Список Лабораторных работ</a>
                    <h2>Список ошибок:</h2>
                    <div class=menu>
                        <ol class='text'>
                            <li><a href="/lab1/400">Код ответа 400</a><br>
                            <li><a href="/lab1/401">Код ответа 401</a><br>
                            <li><a href="/lab1/402">Код ответа 402</a><br>
                            <li><a href="/lab1/403">Код ответа 403</a><br>
                            <li><a href="/lab1/404">Код ответа 404</a><br>
                            <li><a href="/lab1/405">Код ответа 405</a><br>
                            <li><a href="/lab1/418">Код ответа 418</a><br>
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
    css = url_for('static', filename='123.css')
    return """<!doctype html>
        <html> 
        <link rel="stylesheet" href=" """ + css + """ ">
           <body>
                <header>НГТУ, ФБ, WEB-программирование, часть 2.</header>
                    <p>Студент: """ + name + """</p>
                    <p>Группа: """ + group + """</p>
                    <p>Факультет: """ + faculty + """</p>
                    <a href="/lab1/web">web</a>
               <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
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
        </html>''', {
            "X-Server": "sample",
            "X-Content-Language": "en, ru",
            "X-Content-Length": "1234"
        }

count = 0

@app.route("/lab1/counter")
def counter():
    css = url_for('static', filename='123.css')
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
    <!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css + '''">
            <body>
                <header>НГТУ, ФБ, WEB-программирование, часть 2.</header>
                    Сколько раз вы сюда заходили: ''' + str(count) + '''
                    <hr>
                    Дата и время: ''' + str(time) + ''' <br>
                    Запрошенный адрес: ''' + str(url) + ''' <br>
                    Ваш IP-адрес: ''' + str(client_ip) + ''' <br>
                    <hr>
                    <a href="/lab1/reset_counter">Очистить счетчик</a>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>'''

@app.route("/lab1/reset_counter")
def reset_counter():
    css = url_for('static', filename='123.css')
    global count
    count = 0
    return '''
    <!doctype html>
        <html>
        <link rel="stylesheet" href="''' + css + '''">
            <body>
                <header>НГТУ, ФБ, WEB-программирование, часть 2.</header>
                    Счетчик очищен!
                    <hr>
                    <a href="/lab1/counter">Вернуться к счетчику</a>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
            </body>
        </html>'''

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/obrabotch")
def obrabotch():
    css = url_for('static', filename='123.css')
    a = 100
    b = 0
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>''' + str(a/b) + '''</div>
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

@app.route("/lab1/created")
def created():
    css = url_for('static', filename='123.css')
    return '''
<!doctype html>
<html> 
    <link rel="stylesheet" href="''' + css + '''">
    <body>
        <title>НГТУ, ФБ, Лабораторные работы</title>
        <header>НГТУ, ФБ, WEB-программирование, часть 2.</header>
        <h1>Созданно успешно</h1>
        <div><i>что-то созданно...</i></div>
        <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
    </body>
</html>
''', 201

@app.route("/lab1/400")
def code400():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>Код состояния ответа "HTTP 400 Bad Request" указывает, что сервер не смог понять запрос из-за недействительного синтаксиса. Клиент не должен повторять этот запрос без изменений.</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 400

@app.route("/lab1/401")
def code401():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>Код ответа на статус ошибки HTTP 401 Unauthorized клиента указывает, что запрос не был применён, поскольку ему не хватает действительных учётных данных для целевого ресурса.</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 401

@app.route("/lab1/402")
def code402():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>HTTP-ответ 402 Payment Required это нестандартная ошибка клиента, зарезервированная для использования в будущем. Иногда этот код означает, что запрос не может быть выполнен до тех пор, пока клиент не совершит оплату. Изначально создан для активации цифровых средств или (микро) платёжных систем и изображает, что запрошенный контент недоступен пока клиент не совершит оплату. Так или иначе, стандартизованного использования для кода нет, и он может использоваться разными элементами в разном контексте.</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 402

@app.route("/lab1/403")
def code403():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>Код ответа на статус ошибки "HTTP 403 Forbidden" указывает, что сервер понял запрос, но отказывается его авторизовать. Этот статус похож на 401, но в этом случае повторная аутентификация не будет иметь никакого значения. Доступ запрещён и привязан к логике приложения (например, у пользователя не хватает прав доступа к запрашиваемому ресурсу).</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 403

@app.errorhandler(404)
def not_found(err):
    return redirect("/lab1/404")

visit_log = []

@app.route("/lab1/404")
def not_found():
    global visit_log
    
    # Получаем данные о текущем посещении
    client_ip = request.remote_addr
    access_time = datetime.datetime.today()
    requested_url = request.url
    
    # Добавляем запись в лог
    visit_log.append({
        'ip': client_ip,
        'time': access_time,
        'url': requested_url
    })
    
    css = url_for('static', filename='123.css')
    path = url_for("static", filename="2.jpg")
    
    # Формируем HTML с данными
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
    
    # Добавляем записи лога в обратном порядке (последние сверху)
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





@app.route("/lab1/405")
def code405():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>Код состояния протокола HTTP 405 Method Not Allowed, указывает, что метод запроса известен серверу, но был отключён и не может быть использован. Два обязательных метода GET и HEAD никогда не должны быть отключены и не должны возвращать этот код ошибки. Сервер ОБЯЗАН сгенерировать поле заголовка Allow в ответе с кодом 405, которое содержит список текущих доступных методов ресурса.</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 405

@app.route("/lab1/418")
def code418():
    css = url_for('static', filename='123.css')
    return '''<!doctype html>
        <html> 
        <link rel="stylesheet" href="''' + css + '''">
           <body>
                <title>НГТУ, ФБ, Лабораторные работы</title>
                <header>НГТУ, ФБ, WEB-программирование</header>
                <div>HTTP код ошибки 418 I'm a teapot сообщает о том, что «Я — чайник»</div>
                <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
          </body>
        </html>''', 418



@app.route('/lab2/a/')
def z ():
    return 'со слешем'


@app.route('/lab2/a')
def z1 ():
    return 'без слеша'


flower_list = ['роза','тюльпан','незабудка','ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers (flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return "цветок:" + flower_list[flower_id]
    

@app.route('/lab2/add_flower/<name>')
def add_flower (name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html> 
    <body>
    <h1>"Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов цветов: {len(flower_list)}</p>
    <p>Полный список цветов: {flower_list}</p>
    </body>
</html>
'''

@app.route('/lab2/example')
def example():
    name = 'Цеунов Матвей Евгеньевич'
    number_lab = '2'
    group = 'ФБИ-31'
    course = '3'
    return render_template('example.html', name=name, number_lab=number_lab, group=group, course=course)
    


