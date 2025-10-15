from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response
import datetime
lab3 = Blueprint('lab3', __name__)

@lab3.route("/lab3/")
def lab():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route("/lab3/cookie")
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Matvey', max_age=5)
    resp.set_cookie('age', '20 лет')
    resp.set_cookie('name_color', 'red')
    return resp

@lab3.route("/lab3/del_cookie")
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    errors1 = {}
    age = request.args.get('age')
    if age == '':
        errors1['age'] = 'Вы забыли указать возраст!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors, errors1=errors1)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('/lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = 0
    drink = request.args.get('drink')

    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('/lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    cursor = request.args.get('cursor')
    
    if color or bg_color or font_size or cursor:
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if cursor:
            resp.set_cookie('cursor', cursor)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    cursor = request.cookies.get('cursor')
    return render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, cursor=cursor)


@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket.html')

@lab3.route('/lab3/ticket_result')
def ticket_result():
    price = 0

    age = int(request.args.get('age'))
    if age < 18:
        price = 700
        is_child = True
    else:
        price = 1000
        is_child = False

    shelf = request.args.get('shelf')
    if shelf == 'lower' or shelf == 'lower_side':
        price += 100

    if request.args.get('linen') == 'on':
        price += 75

    if request.args.get('luggage') == 'on':
        price += 250

    if request.args.get('insurance') == 'on':
        price += 150

    return render_template('lab3/ticket_result.html', price=price, is_child=is_child,
                         fio=request.args.get('fio'), age=age,
                         departure=request.args.get('departure'),
                         destination=request.args.get('destination'),
                         travel_date=request.args.get('travel_date'))



@lab3.route('/lab3/settings_clear')
def settings_clear():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color')
    resp.delete_cookie('font_size')
    resp.delete_cookie('cursor')
    return resp




products = [
    {"id": 1, "name": "iPhone 15 Pro", "price": 99990, "brand": "Apple", "color": "Титановый", "storage": "128GB"},
    {"id": 2, "name": "Samsung Galaxy S24", "price": 79990, "brand": "Samsung", "color": "Черный", "storage": "256GB"},
    {"id": 3, "name": "Xiaomi 14", "price": 59990, "brand": "Xiaomi", "color": "Белый", "storage": "256GB"},
    {"id": 4, "name": "Google Pixel 8", "price": 54990, "brand": "Google", "color": "Серый", "storage": "128GB"},
    {"id": 5, "name": "OnePlus 12", "price": 64990, "brand": "OnePlus", "color": "Зеленый", "storage": "256GB"},
    {"id": 6, "name": "iPhone 14", "price": 69990, "brand": "Apple", "color": "Синий", "storage": "128GB"},
    {"id": 7, "name": "Samsung Galaxy A54", "price": 34990, "brand": "Samsung", "color": "Фиолетовый", "storage": "128GB"},
    {"id": 8, "name": "Xiaomi Redmi Note 13", "price": 24990, "brand": "Xiaomi", "color": "Черный", "storage": "128GB"},
    {"id": 9, "name": "Realme 11 Pro", "price": 29990, "brand": "Realme", "color": "Золотой", "storage": "256GB"},
    {"id": 10, "name": "Nothing Phone 2", "price": 45990, "brand": "Nothing", "color": "Белый", "storage": "128GB"},
    {"id": 11, "name": "iPhone 15 Pro Max", "price": 129990, "brand": "Apple", "color": "Титановый", "storage": "256GB"},
    {"id": 12, "name": "Samsung Galaxy Z Flip5", "price": 89990, "brand": "Samsung", "color": "Сиреневый", "storage": "256GB"},
    {"id": 13, "name": "Google Pixel 7a", "price": 39990, "brand": "Google", "color": "Голубой", "storage": "128GB"},
    {"id": 14, "name": "Xiaomi Poco X6 Pro", "price": 32990, "brand": "Xiaomi", "color": "Желтый", "storage": "256GB"},
    {"id": 15, "name": "OnePlus Nord 3", "price": 37990, "brand": "OnePlus", "color": "Серый", "storage": "256GB"},
    {"id": 16, "name": "iPhone SE", "price": 44990, "brand": "Apple", "color": "Красный", "storage": "64GB"},
    {"id": 17, "name": "Samsung Galaxy M54", "price": 29990, "brand": "Samsung", "color": "Синий", "storage": "128GB"},
    {"id": 18, "name": "Xiaomi 13T", "price": 49990, "brand": "Xiaomi", "color": "Черный", "storage": "256GB"},
    {"id": 19, "name": "Motorola Edge 40", "price": 41990, "brand": "Motorola", "color": "Зеленый", "storage": "256GB"},
    {"id": 20, "name": "Honor 90", "price": 35990, "brand": "Honor", "color": "Серебристый", "storage": "256GB"}
]

def get_price_range():
    """Получить минимальную и максимальную цену из всех товаров"""
    prices = [product['price'] for product in products]
    return min(prices), max(prices)

@lab3.route('/lab3/products')
def product_search():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    min_price_all, max_price_all = get_price_range()
    
    min_price = request.args.get('min_price', type=int)
    max_price = request.args.get('max_price', type=int)
    reset = request.args.get('reset')
    
    if reset:
        resp = make_response(redirect('/lab3/products'))
        resp.delete_cookie('min_price')
        resp.delete_cookie('max_price')
        return resp
    
    if min_price is not None or max_price is not None:
        resp = make_response(redirect('/lab3/products'))
        if min_price is not None:
            resp.set_cookie('min_price', str(min_price))
        if max_price is not None:
            resp.set_cookie('max_price', str(max_price))
        return resp
    
    if min_price_cookie or max_price_cookie:
        min_price = int(min_price_cookie) if min_price_cookie else None
        max_price = int(max_price_cookie) if max_price_cookie else None
    
    if min_price and max_price and min_price > max_price:
        min_price, max_price = max_price, min_price
        resp = make_response(redirect('/lab3/products'))
        resp.set_cookie('min_price', str(min_price))
        resp.set_cookie('max_price', str(max_price))
        return resp
    
    filtered_products = products
    if min_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] >= min_price]
    if max_price is not None:
        filtered_products = [p for p in filtered_products if p['price'] <= max_price]
    
    for product in filtered_products:
        product['price_formatted'] = f"{product['price']:,}".replace(',', ' ')
    
    return render_template('lab3/products.html',
                         products=filtered_products,
                         min_price=min_price,
                         max_price=max_price,
                         min_price_all=min_price_all,
                         max_price_all=max_price_all,
                         products_count=len(filtered_products),
                         total_products=len(products))