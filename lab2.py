from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime

lab2 = Blueprint('lab2', __name__)


@lab2.route('/lab2/a/')
def z ():
    return 'со слешем'


@lab2.route('/lab2/a')
def z1 ():
    return 'без слеша'


flower_list = [
    {'name': 'роза', 'price': 100},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 30}
]

@lab2.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower = flower_list[flower_id]
        return f"Цветок: {flower['name']}, Цена: {flower['price']} руб."

@lab2.route('/lab2/add_flower/<name>/<int:price>')
def add_flower(name, price):
    flower_list.append({'name': name, 'price': price})
    return f'''
<!doctype html>
<html> 
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name}</p>
    <p>Цена: {price} руб.</p>
    <p>Всего цветов: {len(flower_list)}</p>
    <a href="/lab2/flowerlist">Вернуться к списку цветов</a>
    </body>
</html>
'''

@lab2.route("/lab2/add_flower/")
def none_flower():
    return render_template('none_flower.html')

@lab2.route("/lab2/flowerlist", methods=['GET', 'POST'])
def flowerlist():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name and price:
            flower_list.append({'name': name, 'price': int(price)})
    
    number_flower = len(flower_list)
    return render_template('flowerlist.html', flower_list=flower_list, number_flower=number_flower)

@lab2.route("/lab2/delete_flower/<int:flower_id>")
def delete_flower(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        flower_list.pop(flower_id)
        return redirect('/lab2/flowerlist')

@lab2.route("/lab2/clear_flower")
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



@lab2.route('/lab2/example')
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
    


@lab2.route('/lab2/')
def lab():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = 'О <b>сколько</b> <u>нам</u> <i>отркытий</i> чудных...'
    return render_template('filter.html', phrase=phrase)



@lab2.route("/lab2/calc/<int:a>/<int:b>")
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

@lab2.route("/lab2/calc/")
def defcalc():
    return redirect('/lab2/calc/1/1')

@lab2.route("/lab2/calc/<int:a>")
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

@lab2.route("/lab2/books")
def books():
    return render_template('books.html', 
                        books_list=books_list, 
                        books_count=len(books_list))




@lab2.route("/lab2/cars")
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
    



