from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, jsonify
import json
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, Product, CartItem, Order, OrderItem
from flask_login import login_user, login_required, current_user, logout_user
import functools

rgz = Blueprint('rgz', __name__)

# Вспомогательная функция для JSON-RPC
def jsonrpc(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method != 'POST':
            return jsonify({'error': 'Only POST method is allowed'}), 405
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
            
        if data.get('jsonrpc') != '2.0':
            return jsonify({'error': 'Invalid JSON-RPC version'}), 400
            
        method = data.get('method')
        params = data.get('params', {})
        id = data.get('id')
        
        # Вызываем метод с параметрами
        try:
            result = f(method, params, *args, **kwargs)
            response = {
                'jsonrpc': '2.0',
                'result': result,
                'id': id
            }
            return jsonify(response)
        except Exception as e:
            response = {
                'jsonrpc': '2.0',
                'error': {
                    'code': -32603,
                    'message': str(e)
                },
                'id': id
            }
            return jsonify(response), 500
    
    return decorated_function

# Главная страница
@rgz.route("/rgz/")
def main():
    # Показываем товары
    products = Product.query.limit(12).all()
    return render_template('rgz/rgz.html', products=products, user=current_user)

# Регистрация (уже есть)
@rgz.route('/rgz/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('rgz/register.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('rgz/register.html', error='Пароль не должен быть пустым')
    
    # Валидация логина (только латинские буквы, цифры и некоторые символы)
    import re
    if not re.match(r'^[a-zA-Z0-9_\-\.]+$', login_form):
        return render_template('rgz/register.html', error='Логин может содержать только латинские буквы, цифры, точки, дефисы и подчеркивания')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('rgz/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    return redirect('/rgz/')

# Вход (уже есть)
@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    remember_me = request.form.get('remember') == 'yes'

    if not login_form:
        return render_template('rgz/login.html', error='Имя пользователя не должно быть пустым')
    
    if not password_form:
        return render_template('rgz/login.html', error='Пароль не должен быть пустым')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me)
            return redirect('/rgz/')
        
        return render_template('rgz/login.html', error='Ошибка входа: логин и/или пароль неверны')
    
    return render_template('rgz/login.html', error='Пользователь не найден')

# Выход
@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()
    return redirect('/rgz/')

# Страница корзины
@rgz.route('/rgz/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).join(Product).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('rgz/cart.html', cart_items=cart_items, total=total)

# Удаление аккаунта
@rgz.route('/rgz/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Удаляем корзину пользователя
    CartItem.query.filter_by(user_id=current_user.id).delete()
    # Удаляем пользователя
    user = users.query.get(current_user.id)
    db.session.delete(user)
    db.session.commit()
    logout_user()
    return redirect('/rgz/')

# JSON-RPC API endpoint
@rgz.route('/rgz/api', methods=['POST'])
@login_required
@jsonrpc
def api(method, params):
    if method == 'add_to_cart':
        product_id = params.get('product_id')
        quantity = params.get('quantity', 1)
        
        # Валидация
        if not product_id:
            raise Exception('Product ID is required')
        if quantity <= 0:
            raise Exception('Quantity must be positive')
        
        product = Product.query.get(product_id)
        if not product:
            raise Exception('Product not found')
        
        if product.stock < quantity:
            raise Exception('Not enough stock')
        
        # Проверяем, есть ли уже товар в корзине
        cart_item = CartItem.query.filter_by(
            user_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = CartItem(
                user_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        return {'success': True, 'message': 'Product added to cart'}
    
    elif method == 'remove_from_cart':
        cart_item_id = params.get('cart_item_id')
        
        if not cart_item_id:
            raise Exception('Cart item ID is required')
        
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item or cart_item.user_id != current_user.id:
            raise Exception('Cart item not found')
        
        db.session.delete(cart_item)
        db.session.commit()
        return {'success': True, 'message': 'Product removed from cart'}
    
    elif method == 'update_cart_quantity':
        cart_item_id = params.get('cart_item_id')
        quantity = params.get('quantity')
        
        if not cart_item_id or quantity is None:
            raise Exception('Cart item ID and quantity are required')
        
        if quantity <= 0:
            raise Exception('Quantity must be positive')
        
        cart_item = CartItem.query.get(cart_item_id)
        if not cart_item or cart_item.user_id != current_user.id:
            raise Exception('Cart item not found')
        
        product = cart_item.product
        if product.stock < quantity:
            raise Exception('Not enough stock')
        
        cart_item.quantity = quantity
        db.session.commit()
        return {'success': True, 'message': 'Cart updated'}
    
    elif method == 'get_cart':
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        result = []
        for item in cart_items:
            result.append({
                'id': item.id,
                'product': item.product.to_dict(),
                'quantity': item.quantity,
                'total': item.product.price * item.quantity
            })
        return result
    
    elif method == 'checkout':
        # Получаем товары из корзины
        cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
        
        if not cart_items:
            raise Exception('Cart is empty')
        
        # Проверяем наличие товаров на складе
        for item in cart_items:
            if item.product.stock < item.quantity:
                raise Exception(f'Not enough stock for {item.product.name}')
        
        # Создаем заказ
        total = sum(item.product.price * item.quantity for item in cart_items)
        order = Order(user_id=current_user.id, total_amount=total)
        db.session.add(order)
        db.session.flush()  # Получаем ID заказа
        
        # Добавляем товары в заказ и обновляем склад
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=item.product.price
            )
            db.session.add(order_item)
            
            # Уменьшаем количество на складе
            item.product.stock -= item.quantity
        
        # Очищаем корзину
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        return {
            'success': True, 
            'message': 'Order placed successfully',
            'order_id': order.id,
            'total': total
        }
    
    elif method == 'get_products':
        category = params.get('category')
        search = params.get('search')
        
        query = Product.query
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        
        products = query.limit(params.get('limit', 50)).all()
        return [product.to_dict() for product in products]
    
    else:
        raise Exception(f'Method {method} not found')

# Инициализация товаров (запустить один раз для добавления товаров)
@rgz.route('/rgz/init_products')
def init_products():
    if Product.query.count() > 0:
        return "Products already initialized"
    
    furniture_products = [
        # Диваны
        {'name': 'Угловой диван "Комфорт"', 'description': 'Просторный угловой диван с ортопедическим матрасом', 'price': 45999.99, 'category': 'Диваны', 'stock': 10},
        {'name': 'Прямой диван "Модерн"', 'description': 'Современный диван с регулируемой спинкой', 'price': 32999.99, 'category': 'Диваны', 'stock': 15},
        {'name': 'Диван-кровать "Евро"', 'description': 'Раскладной диван для гостевой комнаты', 'price': 27999.99, 'category': 'Диваны', 'stock': 8},
        
        # Кровати
        {'name': 'Двуспальная кровать "Рояль"', 'description': 'Кровать с ортопедическим основанием и ящиками', 'price': 58999.99, 'category': 'Кровати', 'stock': 7},
        {'name': 'Односпальная кровать "Студент"', 'description': 'Компактная кровать для небольших комнат', 'price': 18999.99, 'category': 'Кровати', 'stock': 12},
        {'name': 'Детская кровать "Радуга"', 'description': 'Яркая кровать с бортиками безопасности', 'price': 22999.99, 'category': 'Кровати', 'stock': 9},
        
        # Столы
        {'name': 'Обеденный стол "Семейный"', 'description': 'Большой стол из массива дуба', 'price': 34999.99, 'category': 'Столы', 'stock': 6},
        {'name': 'Рабочий стол "Офис"', 'description': 'Эргономичный стол с отделениями для проводов', 'price': 15999.99, 'category': 'Столы', 'stock': 20},
        {'name': 'Кофейный столик "Минимал"', 'description': 'Современный журнальный столик со стеклянной столешницей', 'price': 8999.99, 'category': 'Столы', 'stock': 15},
        
        # Стулья
        {'name': 'Офисный стул "Эрго"', 'description': 'Стул с регулируемой высотой и поддержкой поясницы', 'price': 12999.99, 'category': 'Стулья', 'stock': 25},
        {'name': 'Обеденный стул "Классик"', 'description': 'Деревянный стул с мягким сиденьем', 'price': 4999.99, 'category': 'Стулья', 'stock': 30},
        {'name': 'Барный стул "Высота"', 'description': 'Стул для кухонной барной стойки', 'price': 6999.99, 'category': 'Стулья', 'stock': 18},
        
        # Шкафы
        {'name': 'Гардеробный шкаф "Система"', 'description': 'Вместительный шкаф-купе с зеркальными дверями', 'price': 78999.99, 'category': 'Шкафы', 'stock': 5},
        {'name': 'Книжный шкаф "Библиотека"', 'description': 'Шкаф с регулируемыми полками', 'price': 28999.99, 'category': 'Шкафы', 'stock': 8},
        {'name': 'Комод "Практик"', 'description': 'Комод с 5 выдвижными ящиками', 'price': 18999.99, 'category': 'Шкафы', 'stock': 10},
        
        # Кресла
        {'name': 'Кресло-качалка "Релакс"', 'description': 'Деревянное кресло-качалка для отдыха', 'price': 21999.99, 'category': 'Кресла', 'stock': 6},
        {'name': 'Компьютерное кресло "Геймер"', 'description': 'Кресло с поддержкой спины и подголовником', 'price': 24999.99, 'category': 'Кресла', 'stock': 12},
        {'name': 'Кресло-мешок "Бинбэг"', 'description': 'Мягкое кресло-мешок для расслабления', 'price': 7999.99, 'category': 'Кресла', 'stock': 20},
        
        # Полки
        {'name': 'Настенная полка "Модуль"', 'description': 'Набор из 3 модульных полок', 'price': 6999.99, 'category': 'Полки', 'stock': 25},
        {'name': 'Угловая полка "Эконом"', 'description': 'Угловая полка для экономии пространства', 'price': 3999.99, 'category': 'Полки', 'stock': 18},
        
        # Тумбы
        {'name': 'Тумба под ТВ "Медиа"', 'description': 'Тумба с отделениями для техники', 'price': 22999.99, 'category': 'Тумбы', 'stock': 9},
        {'name': 'Прикроватная тумба "Ночник"', 'description': 'Тумба с выдвижным ящиком и полкой', 'price': 8999.99, 'category': 'Тумбы', 'stock': 15},
        
        # Матрасы
        {'name': 'Ортопедический матрас "Здоровье"', 'description': 'Матрас с независимыми пружинами', 'price': 32999.99, 'category': 'Матрасы', 'stock': 7},
        {'name': 'Детский матрас "Антиаллерген"', 'description': 'Гипоаллергенный матрас для детей', 'price': 18999.99, 'category': 'Матрасы', 'stock': 10},
        
        # Светильники
        {'name': 'Люстра "Хрусталь"', 'description': 'Большая люстра с хрустальными подвесками', 'price': 45999.99, 'category': 'Свет', 'stock': 4},
        {'name': 'Настольная лампа "Офис"', 'description': 'Лампа с регулируемым углом наклона', 'price': 2999.99, 'category': 'Свет', 'stock': 30},
        
        # Столы для компьютера
        {'name': 'Игровой стол "Профи"', 'description': 'Стол с местом для системного блока и проводов', 'price': 19999.99, 'category': 'Компьютерные столы', 'stock': 11},
        
        # Диваны для офиса
        {'name': 'Офисный диван "Ресепшн"', 'description': 'Диван для зоны ожидания', 'price': 38999.99, 'category': 'Офисная мебель', 'stock': 6},
        
        # Стеллажи
        {'name': 'Стеллаж "Склад"', 'description': 'Прочный стеллаж для хранения', 'price': 15999.99, 'category': 'Стеллажи', 'stock': 14},
        
        # Пуфы
        {'name': 'Пуф "Оттоманка"', 'description': 'Мягкий пуф с отсеком для хранения', 'price': 8999.99, 'category': 'Пуфы', 'stock': 22},
        
        # Детская мебель
        {'name': 'Детский столик "Творчество"', 'description': 'Стол для рисования и игр', 'price': 7999.99, 'category': 'Детская', 'stock': 16},
        
        # Садовая мебель
        {'name': 'Садовый стол "Патио"', 'description': 'Стол для улицы из влагостойкого материала', 'price': 24999.99, 'category': 'Садовая', 'stock': 8},
    ]
    
    for product_data in furniture_products:
        product = Product(**product_data)
        db.session.add(product)
    
    db.session.commit()
    return "Products initialized successfully"