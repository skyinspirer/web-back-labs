from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response
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