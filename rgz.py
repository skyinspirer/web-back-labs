from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_

rgz = Blueprint('rgz', __name__)


@rgz.route("/rgz/")
def main():
    return render_template('rgz/rgz.html')


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
    

@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()
    return redirect('/rgz/')