from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, jsonify
import json
import time  # ДОБАВЛЕНО: импорт модуля time
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users
from flask_login import login_user, login_required, current_user, logout_user
from functools import wraps

rgz = Blueprint('rgz', __name__)

# Инициализируем список товаров
furniture_items = [
    {"id": 1, "name": "Диван 'Комфорт'", "price": 25000, "category": "Диваны", "image": "rgz/sofa1.jpg", "description": "Мягкий угловой диван с механизмом трансформации"},
    {"id": 2, "name": "Кресло 'Премиум'", "price": 15000, "category": "Кресла", "image": "rgz/armchair1.jpg", "description": "Кожаное кресло с подлокотниками"},
    {"id": 3, "name": "Стол 'Офисный'", "price": 12000, "category": "Столы", "image": "rgz/table1.jpg", "description": "Деревянный офисный стол"},
    {"id": 4, "name": "Стул 'Стандарт'", "price": 3500, "category": "Стулья", "image": "rgz/chair1.jpg", "description": "Офисный стул с регулировкой высоты"},
    {"id": 5, "name": "Шкаф 'Гардероб'", "price": 45000, "category": "Шкафы", "image": "rgz/wardrobe1.jpg", "description": "Трехдверный шкаф-купе"},
    {"id": 6, "name": "Кровать 'Королевская'", "price": 35000, "category": "Кровати", "image": "rgz/bed1.jpg", "description": "Двуспальная кровать с ортопедическим матрасом"},
    {"id": 7, "name": "Тумба 'Прикроватная'", "price": 8000, "category": "Тумбы", "image": "rgz/nightstand1.jpg", "description": "Деревянная прикроватная тумба"},
    {"id": 8, "name": "Комод 'Классик'", "price": 22000, "category": "Комоды", "image": "rgz/dresser1.jpg", "description": "Пятиящичный комод из массива дерева"},
    {"id": 9, "name": "Стеллаж 'Модерн'", "price": 18000, "category": "Стеллажи", "image": "rgz/shelf1.jpg", "description": "Напольный стеллаж с 6 полками"},
    {"id": 10, "name": "Пуфик 'Мини'", "price": 5000, "category": "Пуфы", "image": "rgz/ottoman1.jpg", "description": "Кожаный пуфик для ног"},
    {"id": 11, "name": "Диван 'Евро'", "price": 32000, "category": "Диваны", "image": "rgz/sofa2.png", "description": "Прямой диван еврокнижка"},
    {"id": 12, "name": "Кресло-качалка", "price": 17000, "category": "Кресла", "image": "rgz/rocking_chair.jpg", "description": "Деревянное кресло-качалка"},
    {"id": 13, "name": "Обеденный стол", "price": 28000, "category": "Столы", "image": "rgz/dining_table.jpg", "description": "Раздвижной обеденный стол"},
    {"id": 14, "name": "Барный стул", "price": 4500, "category": "Стулья", "image": "rgz/bar_stool.jpg", "description": "Высокий барный стул"},
    {"id": 15, "name": "Книжный шкаф", "price": 38000, "category": "Шкафы", "image": "rgz/bookcase.jpg", "description": "Шкаф для книг с стеклянными дверцами"},
    {"id": 16, "name": "Кровать односпальная", "price": 22000, "category": "Кровати", "image": "rgz/single_bed.jpg", "description": "Односпальная кровать с ящиками"},
    {"id": 17, "name": "Тумба для обуви", "price": 6500, "category": "Тумбы", "image": "rgz/shoe_cabinet.jpg", "description": "Вместительная тумба для обуви"},
    {"id": 18, "name": "Комод детский", "price": 15000, "category": "Комоды", "image": "rgz/kids_dresser.jpg", "description": "Яркий комод для детской комнаты"},
    {"id": 19, "name": "Стеллаж угловой", "price": 21000, "category": "Стеллажи", "image": "rgz/corner_shelf.jpg", "description": "Угловой стеллаж для книг"},
    {"id": 20, "name": "Пуф со столиком", "price": 12000, "category": "Пуфы", "image": "rgz/ottoman_table.jpg", "description": "Пуф с откидной столешницей"},
    {"id": 21, "name": "Угловой диван", "price": 55000, "category": "Диваны", "image": "rgz/corner_sofa.jpg", "description": "Большой угловой диван"},
    {"id": 22, "name": "Компьютерное кресло", "price": 19000, "category": "Кресла", "image": "rgz/gaming_chair.jpg", "description": "Эргономичное компьютерное кресло"},
    {"id": 23, "name": "Кофейный столик", "price": 15000, "category": "Столы", "image": "rgz/coffee_table.jpg", "description": "Стеклянный кофейный столик"},
    {"id": 24, "name": "Складной стул", "price": 2500, "category": "Стулья", "image": "rgz/folding_chair.jpg", "description": "Металлический складной стул"},
    {"id": 25, "name": "Шкаф-купе", "price": 68000, "category": "Шкафы", "image": "rgz/sliding_wardrobe.jpg", "description": "Встроенный шкаф-купе"},
    {"id": 26, "name": "Двухъярусная кровать", "price": 42000, "category": "Кровати", "image": "rgz/bunk_bed.jpg", "description": "Детская двухъярусная кровать"},
    {"id": 27, "name": "Тумба под TV", "price": 28000, "category": "Тумбы", "image": "rgz/tv_stand.jpg", "description": "Тумба для телевизора"},
    {"id": 28, "name": "Комод с зеркалом", "price": 32000, "category": "Комоды", "image": "rgz/dresser_mirror.jpg", "description": "Туалетный комод с зеркалом"},
    {"id": 29, "name": "Стеллаж для вина", "price": 35000, "category": "Стеллажи", "image": "rgz/wine_rack.jpg", "description": "Стеллаж для хранения вина"},
    {"id": 30, "name": "Пуф-сундук", "price": 8500, "category": "Пуфы", "image": "rgz/chest_ottoman.jpg", "description": "Пуф с отделением для хранения"}
]

# Корзины пользователей (в памяти)
carts = {}

def json_rpc_response(result=None, error=None):
    """Создание JSON-RPC ответа"""
    response = {"jsonrpc": "2.0"}
    if error:
        response["error"] = error
    else:
        response["result"] = result
    return jsonify(response)

def handle_json_rpc(f):
    """Декоратор для обработки JSON-RPC запросов"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return json_rpc_response(error={"code": -32700, "message": "Parse error"})
        
        data = request.get_json()
        
        if not isinstance(data, dict):
            return json_rpc_response(error={"code": -32600, "message": "Invalid Request"})
        
        if data.get("jsonrpc") != "2.0":
            return json_rpc_response(error={"code": -32600, "message": "Invalid Request"})
        
        method = data.get("method")
        params = data.get("params", {})
        id = data.get("id")
        
        # Вызываем метод с параметрами
        result = f(method, params, *args, **kwargs)
        
        if result is None:
            return json_rpc_response(error={"code": -32601, "message": "Method not found"})
        
        if isinstance(result, dict) and "error" in result:
            return json_rpc_response(error=result["error"])
        
        return json_rpc_response(result=result)
    
    return decorated_function

@rgz.route("/rgz/")
def main():
    categories = list(set(item["category"] for item in furniture_items))
    return render_template('rgz/rgz.html', furniture=furniture_items, categories=categories, current_user=current_user)

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

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('rgz/register.html', error='Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)
    return redirect('/rgz/')

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

@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()
    return redirect('/rgz/')

@rgz.route('/rgz/api', methods=['POST'])
@login_required
@handle_json_rpc
def api(method, params):
    """Обработка JSON-RPC API запросов"""
    
    user_id = current_user.id
    
    # Инициализация корзины пользователя
    if user_id not in carts:
        carts[user_id] = []
    
    if method == "get_items":
        # Получение списка товаров с возможностью фильтрации
        category = params.get("category")
        search = params.get("search", "").lower()
        
        items = furniture_items.copy()
        
        if category:
            items = [item for item in items if item["category"] == category]
        
        if search:
            items = [item for item in items 
                    if search in item["name"].lower() 
                    or search in item["description"].lower()]
        
        return items
    
    elif method == "add_to_cart":
        # Добавление товара в корзину
        item_id = params.get("item_id")
        quantity = params.get("quantity", 1)
        
        # Проверка существования товара
        item = next((item for item in furniture_items if item["id"] == item_id), None)
        if not item:
            return {"error": {"code": -32001, "message": "Item not found"}}
        
        # Проверка наличия товара в корзине
        cart_item = next((ci for ci in carts[user_id] if ci["id"] == item_id), None)
        
        if cart_item:
            cart_item["quantity"] += quantity
        else:
            new_cart_item = item.copy()
            new_cart_item["quantity"] = quantity
            carts[user_id].append(new_cart_item)
        
        return {"success": True, "message": "Item added to cart"}
    
    elif method == "remove_from_cart":
        # Удаление товара из корзины
        item_id = params.get("item_id")
        
        carts[user_id] = [item for item in carts[user_id] if item["id"] != item_id]
        
        return {"success": True, "message": "Item removed from cart"}
    
    elif method == "update_cart_item":
        # Обновление количества товара в корзине
        item_id = params.get("item_id")
        quantity = params.get("quantity")
        
        if quantity <= 0:
            return {"error": {"code": -32002, "message": "Quantity must be positive"}}
        
        for item in carts[user_id]:
            if item["id"] == item_id:
                item["quantity"] = quantity
                return {"success": True, "message": "Cart updated"}
        
        return {"error": {"code": -32001, "message": "Item not found in cart"}}
    
    elif method == "get_cart":
        # Получение содержимого корзины
        return carts.get(user_id, [])
    
    elif method == "get_cart_total":
        # Получение общей суммы корзины
        cart = carts.get(user_id, [])
        total = sum(item["price"] * item.get("quantity", 1) for item in cart)
        item_count = sum(item.get("quantity", 1) for item in cart)
        return {"total": total, "item_count": item_count}
    
    elif method == "clear_cart":
        # Очистка корзины
        carts[user_id] = []
        return {"success": True, "message": "Cart cleared"}
    
    elif method == "checkout":
        # Оформление покупки
        cart = carts.get(user_id, [])
        
        if not cart:
            return {"error": {"code": -32003, "message": "Cart is empty"}}
        
        # Генерируем ID заказа
        order_id = f"ORD-{user_id}-{int(time.time())}"
        
        # Очищаем корзину после покупки
        carts[user_id] = []
        
        return {
            "success": True, 
            "message": "Purchase completed successfully",
            "order": {"order_id": order_id}
        }
    
    elif method == "get_categories":
        # Получение списка категорий
        categories = list(set(item["category"] for item in furniture_items))
        return categories
    
    return None  # Метод не найден

@rgz.route('/rgz/cart')
@login_required
def view_cart():
    """Страница просмотра корзины"""
    return render_template('rgz/cart.html', current_user=current_user)

@rgz.route('/rgz/checkout')
@login_required
def checkout_page():
    """Страница оформления заказа"""
    return render_template('rgz/checkout.html', current_user=current_user)

@rgz.route('/rgz/order-confirmation/<order_id>')
@login_required
def order_confirmation(order_id):
    """Простая страница подтверждения заказа"""
    return render_template('rgz/order_confirmation.html', order_id=order_id)