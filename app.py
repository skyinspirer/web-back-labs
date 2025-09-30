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
                    <div><a href="/lab2">Лабораторная работа №2</a></div>
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

@app.route("/lab2/add_flower/")
def none_flower():
    return render_template('none_flower.html')

@app.route("/lab2/flowerlist")
def flowerlist():
    number_flower = len(flower_list)
    return render_template('flowerlist.html', flower_list=flower_list, number_flower=number_flower)

@app.route("/lab2/clear_flower")
def clear_flower():
    css = url_for('static', filename='123.css') 
    flower_list.clear()
    return f'''<!doctype html>
            <html>
            <link rel="stylesheet" href="{css}">
            <body>
                    <title>НГТУ, ФБ, Лабораторная работа 2</title>
                    <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
                    <div>Список очищен</div>
                    <footer>Цеунов Матвей Евгегьевич, ФБИ-31, 3 курс, 2025</footer>
                    <a href='/lab2/flowerlist'>Список цветов </a>
            </body>
            </html>'''



@app.route('/lab2/example')
def example():
    name = 'Цеунов Матвей Евгеньевич'
    number_lab = '2'
    group = 'ФБИ-31'
    course = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},    
        {'name': 'апельсины', 'price': 80},    
        {'name': 'мандарины', 'price': 95},    
        {'name': 'манго', 'price': 321}        
    ]
    return render_template('example.html', name=name, number_lab=number_lab, group=group, course=course, fruits=fruits)
    


@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@app.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>отркытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)



@app.route("/lab2/calc/<int:a>/<int:b>")
def calc(a, b):
    css = url_for('static', filename='123.css')
    
    sum = a + b
    minus = a - b
    umn = a * b
    stepen = a ** b
    stepen_str = f"{a}<sup>{b}</sup> = {stepen}"
    
    if b != 0:
        delenie = a / b
        delenie_str = f"{a} / {b} = {delenie}"
    else:
        delenie_str = f"{a} / {b} = деление на 0 запрещено!"
    
    
    return f'''<!doctype html>
        <html>
        <link rel="stylesheet" href="{css}">
        <body>
            <title>НГТУ, ФБ, Лабораторная работа 2</title>
            <header>НГТУ, ФБ, WEB-программирование, Лабораторная 2</header>
            <h2>Калькулятор</h2>
            <div>Число a: {a}</div>
            <div>Число b: {b}</div>
            <hr>
            <div>Сумма: {a} + {b} = {sum}</div>
            <div>Вычитание: {a} - {b} = {minus}</div>
            <div>Умножение: {a} * {b} = {umn}</div>
            <div>Деление: {delenie_str}</div>
            <div>Возведение в степень: {stepen_str}</div>
            <hr>
            <footer>Цеунов Матвей Евгеньевич, ФБИ-31, 3 курс, 2025</footer>
        </body>
        </html>'''

@app.route("/lab2/calc/")
def defcalc():
    return redirect('/lab2/calc/1/1')

@app.route("/lab2/calc/<int:a>")
def newcalc(a):
    return redirect(f'/lab2/calc/{a}/1')

books_list = [
        {"author": "Фёдор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
        {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман-эпопея", "pages": 1225},
        {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастика", "pages": 480},
        {"author": "Антон Чехов", "title": "Рассказы", "genre": "Рассказы", "pages": 320},
        {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Роман в стихах", "pages": 240},
        {"author": "Николай Гоголь", "title": "Мёртвые души", "genre": "Поэма", "pages": 352},
        {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 288},
        {"author": "Александр Островский", "title": "Гроза", "genre": "Драма", "pages": 128},
        {"author": "Михаил Лермонтов", "title": "Герой нашего времени", "genre": "Роман", "pages": 224},
        {"author": "Иван Гончаров", "title": "Обломов", "genre": "Роман", "pages": 576},
        {"author": "Александр Грибоедов", "title": "Горе от ума", "genre": "Комедия", "pages": 160},
        {"author": "Николай Лесков", "title": "Левша", "genre": "Повесть", "pages": 96}
    ]

@app.route("/lab2/books")
def books():
    return render_template('books.html', 
                        books_list=books_list, 
                        books_count=len(books_list))




@app.route("/lab2/cars")
def cars():
    cars_list = [
        {
            "name": "Toyota Camry", 
            "brand": "Toyota", 
            "year": 2023, 
            "engine": "2.5L Hybrid", 
            "power": 218, 
            "price": "3 200 000 ₽",
            "description": "Современный седан с гибридной установкой, экономичный и комфортный.",
            "image": "toyota_camry.png"
        },
        {
            "name": "BMW X5", 
            "brand": "BMW", 
            "year": 2024, 
            "engine": "3.0L Turbo", 
            "power": 340, 
            "price": "7 500 000 ₽",
            "description": "Премиальный кроссовер с отличной динамикой и роскошным интерьером.",
            "image": "bmw_x5.png"
        },
        {
            "name": "Mercedes-Benz S-Class", 
            "brand": "Mercedes-Benz", 
            "year": 2023, 
            "engine": "3.0L Hybrid", 
            "power": 367, 
            "price": "12 000 000 ₽",
            "description": "Флагманский седан класса люкс с инновационными технологиями.",
            "image": "mercedes_s_class.png"
        },
        {
            "name": "Audi A6", 
            "brand": "Audi", 
            "year": 2023, 
            "engine": "2.0L TFSI", 
            "power": 245, 
            "price": "4 800 000 ₽",
            "description": "Бизнес-седан с фирменной оптикой и качественной отделкой.",
            "image": "audi_a6.png"
        },
        {
            "name": "Volkswagen Tiguan", 
            "brand": "Volkswagen", 
            "year": 2023, 
            "engine": "2.0L TSI", 
            "power": 190, 
            "price": "3 500 000 ₽",
            "description": "Популярный кроссовер с практичным салоном и надежной техникой.",
            "image": "vw_tiguan.png"
        },
        {
            "name": "Hyundai Tucson", 
            "brand": "Hyundai", 
            "year": 2024, 
            "engine": "1.6L Turbo", 
            "power": 180, 
            "price": "2 900 000 ₽",
            "description": "Стильный кроссовер с агрессивным дизайном и богатой комплектацией.",
            "image": "hyundai_tucson.png"
        },
        {
            "name": "Kia Sportage", 
            "brand": "Kia", 
            "year": 2023, 
            "engine": "1.6L Turbo", 
            "power": 180, 
            "price": "2 800 000 ₽",
            "description": "Компактный кроссовер с ярким дизайном и передовыми системами.",
            "image": "kia_sportage.png"
        },
        {
            "name": "Lada Vesta", 
            "brand": "Lada", 
            "year": 2024, 
            "engine": "1.6L", 
            "power": 106, 
            "price": "1 300 000 ₽",
            "description": "Народный автомобиль с обновленным дизайном и доступной ценой.",
            "image": "lada_vesta.png"
        },
        {
            "name": "Skoda Octavia", 
            "brand": "Skoda", 
            "year": 2023, 
            "engine": "1.4L TSI", 
            "power": 150, 
            "price": "2 400 000 ₽",
            "description": "Практичный лифтбек с огромным багажником и экономичным мотором.",
            "image": "skoda_octavia.png"
        },
        {
            "name": "Ford Focus", 
            "brand": "Ford", 
            "year": 2023, 
            "engine": "1.5L EcoBoost", 
            "power": 150, 
            "price": "2 200 000 ₽",
            "description": "Динамичный хэтчбек с отличной управляемостью и современной электроникой.",
            "image": "ford_focus.png"
        },
        {
            "name": "Nissan Qashqai", 
            "brand": "Nissan", 
            "year": 2024, 
            "engine": "1.3L Turbo", 
            "power": 140, 
            "price": "2 700 000 ₽",
            "description": "Первый в мире кроссовер-компакт, обновленная версия популярной модели.",
            "image": "nissan_qashqai.png"
        },
    ]
    
    return render_template('cars.html', 
                        cars_list=cars_list, 
                        cars_count=len(cars_list))
    



