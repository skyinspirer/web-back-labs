from flask import Blueprint, render_template, request, jsonify, abort
from datetime import datetime
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html') 

def db_connect():
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM films")
    films = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = db_connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    film = cur.fetchone()
    conn.close()
    
    if not film:
        abort(404, description="Фильм не найден")
    return jsonify(dict(film))

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn = db_connect()
    cur = conn.cursor()
    
    # Сначала проверяем, существует ли фильм
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    if not cur.fetchone():
        conn.close()
        abort(404, description="Фильм не найден")
    
    cur.execute("DELETE FROM films WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film_data = request.get_json()
    errors = {}
    
    # Проверка русского названия
    if not film_data.get('title_ru'):
        errors['description'] = 'Заполните русское название'
    
    # Если оригинальное пустое - копируем русское
    if not film_data.get('title'):
        film_data['title'] = film_data.get('title_ru', '')
    
    # Проверка года
    if not film_data.get('year'):
        errors['description'] = 'Укажите год'
    else:
        try:
            year = int(film_data['year'])
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['description'] = f'Год должен быть от 1895 до {current_year}'
        except ValueError:
            errors['description'] = 'Год должен быть числом'
    
    # Проверка описания
    if not film_data.get('description'):
        errors['description'] = 'Заполните описание'
    elif len(film_data.get('description', '')) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    conn = db_connect()
    cur = conn.cursor()
    
    # Проверяем, существует ли фильм
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    existing_film = cur.fetchone()
    if not existing_film:
        conn.close()
        abort(404, description="Фильм не найден")
    
    # Обновляем фильм
    cur.execute("""
        UPDATE films 
        SET title = ?, title_ru = ?, year = ?, description = ?
        WHERE id = ?
    """, (film_data['title'], film_data['title_ru'], film_data['year'], 
          film_data['description'], id))
    conn.commit()
    
    # Получаем обновленный фильм
    cur.execute("SELECT * FROM films WHERE id = ?", (id,))
    updated_film = cur.fetchone()
    conn.close()
    
    return jsonify(dict(updated_film))

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film_data = request.get_json()
    errors = {}
    
    # Проверка русского названия
    if not film_data.get('title_ru'):
        errors['description'] = 'Заполните русское название'
    
    # Если оригинальное пустое - копируем русское
    if not film_data.get('title'):
        film_data['title'] = film_data.get('title_ru', '')
    
    # Проверка года
    if not film_data.get('year'):
        errors['description'] = 'Укажите год'
    else:
        try:
            year = int(film_data['year'])
            current_year = datetime.now().year
            if year < 1895 or year > current_year:
                errors['description'] = f'Год должен быть от 1895 до {current_year}'
        except ValueError:
            errors['description'] = 'Год должен быть числом'
    
    # Проверка описания
    if not film_data.get('description'):
        errors['description'] = 'Заполните описание'
    elif len(film_data.get('description', '')) > 2000:
        errors['description'] = 'Описание должно быть не более 2000 символов'
    
    if errors:
        return jsonify(errors), 400
    
    conn = db_connect()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO films (title, title_ru, year, description)
        VALUES (?, ?, ?, ?)
    """, (film_data['title'], film_data['title_ru'], 
          film_data['year'], film_data['description']))
    
    film_id = cur.lastrowid
    conn.commit()
    
    # Получаем созданный фильм
    cur.execute("SELECT * FROM films WHERE id = ?", (film_id,))
    new_film = cur.fetchone()
    conn.close()
    
    return jsonify(dict(new_film)), 201