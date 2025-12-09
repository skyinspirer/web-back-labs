from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session, current_app, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

def db_connect():
    """Подключение к базе данных (PostgreSQL или SQLite)"""
    # Для простоты используем SQLite локально
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "films.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    """Закрытие соединения с базой данных"""
    conn.commit()
    cur.close()
    conn.close()

def init_db():
    """Инициализация базы данных при первом запуске"""
    conn, cur = db_connect()
    
    # Создаем таблицу фильмов
    cur.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            title_ru TEXT NOT NULL,
            year INTEGER NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Проверяем, есть ли данные в таблице
    cur.execute("SELECT COUNT(*) FROM films")
    count = cur.fetchone()[0]
    
    # Если таблица пустая, добавляем тестовые данные
    if count == 0:
        test_films = [
            ("1 + 1", "1+1", 2011, "Пострадав в результате несчастного случая, богатый аристократ Филипп нанимает в помощники человека, который менее всего подходит для этой работы, – молодого жителя предместья Дрисса, только что освободившегося из тюрьмы."),
            ("Interstellar", "Интерстеллар", 2014, "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие."),
            ("The Gentlemen", "Джентльмены", 2019, "Один ушлый американец ещё со студенческих лет приторговывал наркотиками, а теперь придумал схему нелегального обогащения с использованием поместий обедневшей английской аристократии.")
        ]
        cur.executemany(
            'INSERT INTO films (title, title_ru, year, description) VALUES (?, ?, ?, ?)',
            test_films
        )
    
    db_close(conn, cur)

# Инициализируем БД при импорте
init_db()

@lab7.route("/lab7/")
def main():
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    
    cur.execute("SELECT * FROM films ORDER BY id;")
    films = cur.fetchall()
    db_close(conn, cur)
    
    films_list = []
    for film in films:
        films_list.append(dict(film))
    
    return jsonify(films_list)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    
    cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    
    if not film:
        abort(404)
    
    return dict(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    
    cur.execute("SELECT title_ru FROM films WHERE id = ?;", (id,))
    film = cur.fetchone()
    
    if not film:
        db_close(conn, cur)
        abort(404)
    
    cur.execute("DELETE FROM films WHERE id = ?;", (id,))
    db_close(conn, cur)
    
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    errors = {}
    
    # Проверка title_ru
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название обязательно для заполнения'
    
    # Если оригинальное название пустое, используем русское
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    # Проверка года
    year = film.get('year')
    if year is None or year == '':
        errors['year'] = 'Год обязателен для заполнения'
    else:
        try:
            year_int = int(year)
            if year_int < 1895:
                errors['year'] = 'Год не может быть раньше 1895'
            elif year_int > 2025:
                errors['year'] = 'Год не может быть больше 2025'
        except:
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    description = film.get('description', '')
    if description == '':
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()

    cur.execute("SELECT id FROM films WHERE id = ?;", (id,))
    if not cur.fetchone():
        db_close(conn, cur)
        abort(404)
    
    # Обновляем фильм
    cur.execute("""
        UPDATE films 
        SET title = ?, title_ru = ?, year = ?, description = ? 
        WHERE id = ?;
    """, (film['title'], film['title_ru'], year_int, description, id))
    
    cur.execute("SELECT * FROM films WHERE id = ?;", (id,))
    updated_film = cur.fetchone()
    
    db_close(conn, cur)
    
    return dict(updated_film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    errors = {}
    
    if not film.get('title_ru'):
        errors['title_ru'] = 'Русское название обязательно для заполнения'
    
    if not film.get('title') and film.get('title_ru'):
        film['title'] = film['title_ru']
    
    year = film.get('year')
    if year is None or year == '':
        errors['year'] = 'Год обязателен для заполнения'
    else:
        try:
            year_int = int(year)
            if year_int < 1895:
                errors['year'] = 'Год не может быть раньше 1895'
            elif year_int > 2025:
                errors['year'] = 'Год не может быть больше 2025'
        except:
            errors['year'] = 'Год должен быть числом'
    
    description = film.get('description', '')
    if description == '':
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    
    # Добавляем новый фильм
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description) 
        VALUES (?, ?, ?, ?);
    """, (film['title'], film['title_ru'], year_int, description))
    
    cur.execute("SELECT last_insert_rowid() as id;")
    new_id = cur.fetchone()['id']
    
    db_close(conn, cur)
    
    return str(new_id), 201