from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session
import datetime
lab4 = Blueprint ('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

    
@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    if x2 == '0':
        return render_template('lab4/div.html', error='Делить на ноль нельзя!')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/summa", methods = ['POST'])
def summa():
    x1 = request.form.get('x1') or '0'
    x2 = request.form.get('x2') or '0'

    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2

    return render_template('lab4/summa.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/ymnoshenie", methods = ['POST'])
def ymnoshenie():
    x1 = request.form.get('x1') or '1'
    x2 = request.form.get('x2') or '1'

    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2

    return render_template('lab4/ymnoshenie.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/vichitanie", methods = ['POST'])
def vichitanie():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/vichitanie.html', error='Оба значения должны быть заполнены')


    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2

    return render_template('lab4/vichitanie.html', x1=x1, x2=x2, result=result)


@lab4.route("/lab4/stepen", methods = ['POST'])
def stepen():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')

    if x1 == '' or x2 == '':
        return render_template('lab4/stepen.html', error='Оба значения должны быть заполнены')

    if x1 == '0' and x2 == '0':
        return render_template('lab4/stepen.html', error='Оба поля не должны равняться 0')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2

    return render_template('lab4/stepen.html', x1=x1, x2=x2, result=result)


tree_count = 0
@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    if request.method == 'POST':
        operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр Александрович'},
    {'login': 'bob', 'password': '555', 'name': 'Боби Петрович'},
    {'login': 'matvey', 'password': '403', 'name': 'Матвей Евгеньевич'},
    {'login': 'artem', 'password': '984', 'name': 'Артем Евгеньевич'},
    {'login': 'sanek', 'password': '432', 'name': 'Александр Алексеевич'},
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            name = ''
            for user in users:
                if user['login'] == login:
                    name = user['name']
        else:
            authorized = False
            name = ''
        return render_template('lab4/login.html', authorized=authorized, name=name)

    
    login = request.form.get('login')
    password = request.form.get('password')

    if login == '':
        errorlogin = 'Не введён логин!'
        return render_template('lab4/login.html', errorlogin=errorlogin, authorized=False)
    
    if password == '':
        errorpassword = 'Не введён пароль!'
        return render_template('lab4/login.html', errorpassword=errorpassword, authorized=False)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False)



@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/holodos', methods=['GET', 'POST'])
def holodos():
    temperature = None
    error = None
    snowflakes = 0
    
    if request.method == 'POST':
        temp_input = request.form.get('temperature')
        
        # Проверка на пустое значение
        if not temp_input:
            error = 'ошибка: не задана температура'
            return render_template('lab4/holodos.html', temperature=temperature, error=error, snowflakes=snowflakes)
        
        # Проверка что введено число
        if not temp_input.lstrip('-').isdigit():
            error = 'ошибка: введите целое число'
            return render_template('lab4/holodos.html', temperature=temperature, error=error, snowflakes=snowflakes)
        
        temperature = int(temp_input)
        
        # Проверка диапазонов температуры
        if temperature < -12:
            error = 'не удалось установить температуру — слишком низкое значение'
            return render_template('lab4/holodos.html', temperature=temperature, error=error, snowflakes=snowflakes)
        
        if temperature > -1:
            error = 'не удалось установить температуру — слишком высокое значение'
            return render_template('lab4/holodos.html', temperature=temperature, error=error, snowflakes=snowflakes)
        
        # Установка корректной температуры
        if -12 <= temperature <= -9:
            snowflakes = 3
        elif -8 <= temperature <= -5:
            snowflakes = 2
        elif -4 <= temperature <= -1:
            snowflakes = 1
    
    return render_template('lab4/holodos.html', temperature=temperature, error=error, snowflakes=snowflakes)


@lab4.route('/lab4/grain_order', methods=['GET', 'POST'])
def grain_order():
    grain_type = None
    weight = None
    total_price = None
    error = None
    discount_applied = False
    discount_amount = 0
    
    prices = {
        'barley': 12000,  
        'oats': 8500,     
        'wheat': 9000,    
        'rye': 15000      
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс', 
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight_input = request.form.get('weight')
        
        # Проверка на пустой вес
        if not weight_input:
            error = 'Ошибка: не указан вес заказа'
        
        # Проверка что введено число 
        elif not weight_input.replace('.', '', 1).replace(',', '', 1).isdigit():
            error = 'Ошибка: введите корректное число для веса'
        
        else:
            # Замена запятой на точку для корректного преобразования
            weight_input = weight_input.replace(',', '.')
            weight = float(weight_input)
            
            # Проверка на отрицательный или нулевой вес
            if weight <= 0:
                error = 'Ошибка: вес должен быть больше 0'
            
            # Проверка на слишком большой объем
            elif weight > 100:
                error = 'Извините, такого объёма сейчас нет в наличии'
            
            else:
                # Проверка выбора зерна
                if not grain_type:
                    error = 'Ошибка: не выбрано зерно'
                
                else:
                    # Расчет стоимости
                    price_per_ton = prices.get(grain_type)
                    total_price = weight * price_per_ton
                    
                    # Применение скидки за большой объем
                    if weight > 10:
                        discount_amount = total_price * 0.1
                        total_price -= discount_amount
                        discount_applied = True
    
    return render_template('lab4/grain_order.html', grain_type=grain_type, weight=weight, total_price=total_price, error=error, discount_applied=discount_applied, discount_amount=discount_amount, grain_names=grain_names)