from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab3 = Blueprint('lab3', __name__)

@lab3.route("/lab3/")
def lab():
    name = request.cookies.get('name')
    return render_template('lab3/lab3.html', name=name)


@lab3.route("/lab3/cookie")
def cookie():
    return 'Установка cookie', 200, {'Set-Cookie': 'name=Alex'}
