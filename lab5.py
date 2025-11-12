from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, flash
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path 

lab5 = Blueprint('lab5', __name__)

@lab5.route("/lab5/")
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='tseunov_matvey_knowledge_base',
            user='tseunov_matvey_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route("/lab5/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    real_name = request.form.get('real_name', '').strip()

    if not (login and password):
        return render_template('lab5/register.html', error='Заполните все обязательные поля')
    
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
        else: 
            cur.execute("SELECT login FROM users WHERE login=?;", (login,))

        if cur.fetchone():
            db_close(conn, cur)
            return render_template('lab5/register.html', error='Такой пользователь уже существует')
        
        password_hash = generate_password_hash(password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (%s, %s, %s);", 
                       (login, password_hash, real_name))
        else: 
            cur.execute("INSERT INTO users (login, password, real_name) VALUES (?, ?, ?);", 
                       (login, password_hash, real_name))
        
        db_close(conn, cur)
        return render_template('lab5/success.html', login=login)
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/register.html', error='Ошибка при регистрации')

@lab5.route("/lab5/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login and password):
        return render_template('lab5/login.html', error='Заполните поля')
    
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
        else: 
            cur.execute("SELECT * FROM users WHERE login=?;", (login,))
        user = cur.fetchone()

        if not user:
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html', error='Логин и/или пароль неверны')
        
        session['login'] = login
        session['user_id'] = user['id']
        session['real_name'] = user.get('real_name', '')
        db_close(conn, cur)
        return redirect('/lab5')
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Ошибка при входе')

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('real_name', None)
    return redirect('/lab5')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = bool(request.form.get('is_favorite'))
    is_public = bool(request.form.get('is_public'))

    # Валидация
    if not title:
        return render_template('lab5/create_article.html', error='Название статьи не может быть пустым')
    if not article_text:
        return render_template('lab5/create_article.html', error='Текст статьи не может быть пустым')
    if len(title) > 100:
        return render_template('lab5/create_article.html', error='Название статьи слишком длинное')

    conn, cur = db_connect()

    try:
        user_id = session.get('user_id')
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) 
                VALUES (%s, %s, %s, %s, %s);
            """, (user_id, title, article_text, is_favorite, is_public))
        else:
            cur.execute("""
                INSERT INTO articles(user_id, title, article_text, is_favorite, is_public) 
                VALUES (?, ?, ?, ?, ?);
            """, (user_id, title, article_text, is_favorite, is_public))

        db_close(conn, cur)
        return redirect('/lab5/list')
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/create_article.html', error='Ошибка при создании статьи')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    
    conn, cur = db_connect()

    try:
        #  запрос для получения всех публичных статей
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE is_public = TRUE ORDER BY id DESC;")
        else:
            cur.execute("SELECT * FROM articles WHERE is_public = TRUE ORDER BY id DESC;")
        
        articles = cur.fetchall()
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=articles, login=login)
    except Exception as e:
        db_close(conn, cur)
        return render_template('/lab5/articles.html', articles=[], login=login)

@lab5.route('/lab5/my_articles')
def my_articles():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        user_id = session.get('user_id')

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id=%s 
                ORDER BY is_favorite DESC, id DESC;
            """, (user_id,))
        else:
            cur.execute("""
                SELECT * FROM articles 
                WHERE user_id=? 
                ORDER BY is_favorite DESC, id DESC;
            """, (user_id,))
        
        articles = cur.fetchall()
        db_close(conn, cur)
        return render_template('/lab5/my_articles.html', articles=articles, login=login)
    except Exception as e:
        db_close(conn, cur)
        return render_template('/lab5/my_articles.html', articles=[], login=login)

@lab5.route('/lab5/article/<int:article_id>')
def view_article(article_id):
    login = session.get('login')
    
    conn, cur = db_connect()

    try:
        # Получаем статью с информацией об авторе
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT a.*, u.login as author, u.real_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.id=%s AND (a.is_public = TRUE OR u.id = %s);
            """, (article_id, session.get('user_id', 0)))
        else:
            cur.execute("""
                SELECT a.*, u.login as author, u.real_name 
                FROM articles a 
                JOIN users u ON a.user_id = u.id 
                WHERE a.id=? AND (a.is_public = TRUE OR u.id = ?);
            """, (article_id, session.get('user_id', 0)))
        
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return render_template('lab5/article_not_found.html')

        # Проверяем, является ли пользователь автором статьи
        is_author = False
        if login:
            user_id = session.get('user_id')
            is_author = (user_id == article['user_id'])

        db_close(conn, cur)
        return render_template('lab5/view_article.html', article=article, login=login, is_author=is_author)

    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/article_not_found.html')

@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        user_id = session.get('user_id')

        # Проверяем, принадлежит ли статья пользователю
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
        
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return redirect('/lab5/my_articles')

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('lab5/edit_article.html', article=article)

        # Обработка формы редактирования
        title = request.form.get('title', '').strip()
        article_text = request.form.get('article_text', '').strip()
        is_favorite = bool(request.form.get('is_favorite'))
        is_public = bool(request.form.get('is_public'))

        # Валидация
        if not title:
            return render_template('lab5/edit_article.html', article=article, error='Название статьи не может быть пустым')
        if not article_text:
            return render_template('lab5/edit_article.html', article=article, error='Текст статьи не может быть пустым')
        if len(title) > 100:
            return render_template('lab5/edit_article.html', article=article, error='Название статьи слишком длинное')

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                UPDATE articles 
                SET title=%s, article_text=%s, is_favorite=%s, is_public=%s 
                WHERE id=%s;
            """, (title, article_text, is_favorite, is_public, article_id))
        else:
            cur.execute("""
                UPDATE articles 
                SET title=?, article_text=?, is_favorite=?, is_public=? 
                WHERE id=?;
            """, (title, article_text, is_favorite, is_public, article_id))

        db_close(conn, cur)
        return redirect('/lab5/article/' + str(article_id))

    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article, error='Ошибка при редактировании статьи')

@lab5.route('/lab5/delete/<int:article_id>', methods=['GET', 'POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        user_id = session.get('user_id')

        # Проверяем, принадлежит ли статья пользователю
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
        
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return redirect('/lab5/my_articles')

        if request.method == 'GET':
            db_close(conn, cur)
            return render_template('lab5/delete_article.html', article=article)

        # Подтверждение удаления
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("DELETE FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
        else:
            cur.execute("DELETE FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))

        db_close(conn, cur)
        return redirect('/lab5/my_articles')

    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/delete_article.html', article=article, error='Ошибка при удалении статьи')

# Новые маршруты для дополнительных заданий

@lab5.route('/lab5/users')
def users_list():
    login = session.get('login')
    
    conn, cur = db_connect()

    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT id, login, real_name FROM users ORDER BY login;")
        else:
            cur.execute("SELECT id, login, real_name FROM users ORDER BY login;")
        
        users = cur.fetchall()
        db_close(conn, cur)
        return render_template('lab5/users_list.html', users=users, login=login)
    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/users_list.html', users=[], login=login)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/profile.html', 
                             login=login, 
                             real_name=session.get('real_name', ''))

    # Обработка изменения профиля
    new_real_name = request.form.get('real_name', '').strip()
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')

    conn, cur = db_connect()

    try:
        user_id = session.get('user_id')

        # Получаем текущие данные пользователя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM users WHERE id=%s;", (user_id,))
        else:
            cur.execute("SELECT * FROM users WHERE id=?;", (user_id,))
        
        user = cur.fetchone()

        errors = []

        # Проверка текущего пароля если меняется пароль
        if new_password:
            if not current_password:
                errors.append('Для смены пароля введите текущий пароль')
            elif not check_password_hash(user['password'], current_password):
                errors.append('Текущий пароль неверен')
            elif new_password != confirm_password:
                errors.append('Новый пароль и подтверждение не совпадают')
            elif len(new_password) < 3:
                errors.append('Новый пароль слишком короткий')

        if errors:
            db_close(conn, cur)
            return render_template('lab5/profile.html', 
                                 login=login, 
                                 real_name=session.get('real_name', ''),
                                 errors=errors)

        # Обновляем данные
        if new_password:
            # Меняем и имя и пароль
            password_hash = generate_password_hash(new_password)
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("""
                    UPDATE users 
                    SET real_name=%s, password=%s 
                    WHERE id=%s;
                """, (new_real_name, password_hash, user_id))
            else:
                cur.execute("""
                    UPDATE users 
                    SET real_name=?, password=? 
                    WHERE id=?;
                """, (new_real_name, password_hash, user_id))
        else:
            # Меняем только имя
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE users SET real_name=%s WHERE id=%s;", (new_real_name, user_id))
            else:
                cur.execute("UPDATE users SET real_name=? WHERE id=?;", (new_real_name, user_id))

        # Обновляем сессию
        session['real_name'] = new_real_name

        db_close(conn, cur)
        return render_template('lab5/profile_success.html', login=login)

    except Exception as e:
        db_close(conn, cur)
        return render_template('lab5/profile.html', login=login, real_name=session.get('real_name', ''), errors=['Ошибка при обновлении профиля'])

@lab5.route('/lab5/toggle_favorite/<int:article_id>')
def toggle_favorite(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    conn, cur = db_connect()

    try:
        user_id = session.get('user_id')

        # Проверяем, принадлежит ли статья пользователю
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;", (article_id, user_id))
        else:
            cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;", (article_id, user_id))
        
        article = cur.fetchone()

        if not article:
            db_close(conn, cur)
            return redirect('/lab5/my_articles')

        # Переключаем статус избранного
        new_favorite_status = not article['is_favorite']
        
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE articles SET is_favorite=%s WHERE id=%s;", (new_favorite_status, article_id))
        else:
            cur.execute("UPDATE articles SET is_favorite=? WHERE id=?;", (new_favorite_status, article_id))

        db_close(conn, cur)
        return redirect('/lab5/my_articles')

    except Exception as e:
        db_close(conn, cur)
        return redirect('/lab5/my_articles')