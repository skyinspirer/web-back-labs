from flask import Blueprint, url_for, request, redirect, abort, render_template, make_response, session
import datetime
lab7 = Blueprint('lab7', __name__)

@lab7.route("/lab7/")
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "1 + 1",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Пострадав в результате несчастного случая, богатый аристократ Филипп \
            нанимает в помощники человека, который менее всего подходит для этой \
            работы, – молодого жителя предместья Дрисса, только что освободившегося\
            из тюрьмы. Несмотря на то, что Филипп прикован к инвалидному креслу,\
            Дриссу удается привнести в размеренную жизнь аристократа дух приключений."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар ",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к\
            продовольственному кризису, коллектив исследователей и учёных\
            отправляется сквозь червоточину (которая предположительно соединяет\
            области пространства-времени через большое расстояние) в путешествие,\
            чтобы превзойти прежние ограничения для космических путешествий\
            человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Gentlemen",
        "title_ru": "Джентльмены",
        "year": 2019,
        "description": "Один ушлый американец ещё со студенческих лет приторговывал\
            наркотиками, а теперь придумал схему нелегального обогащения\
            с использованием поместий обедневшей английской аристократии и очень\
            неплохо на этом разбогател. Другой пронырливый журналист приходит к Рэю,\
            правой руке американца, и предлагает тому купить киносценарий, в котором\
            подробно описаны преступления его босса при участии других к себе расположения.\
            представителей лондонского криминального мира — партнёра-еврея,\
            китайской диаспоры, чернокожих спортсменов и даже русского олигарха."
    }
]


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)

    return films[id]


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
        
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
        
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
    if year is None:
        errors['year'] = 'Год обязателен для заполнения'
    else:
        try:
            year_int = int(year)
            if year_int < 1895:
                errors['year'] = 'Год не может быть раньше 1895'
            elif year_int > 2025:
                errors['year'] = 'Год не может быть больше 2025'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    description = film.get('description', '')
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    if errors:
        return errors, 400

    films[id] = film
    return films[id], 200


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
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
    if year is None:
        errors['year'] = 'Год обязателен для заполнения'
    else:
        try:
            year_int = int(year)
            if year_int < 1895:
                errors['year'] = 'Год не может быть раньше 1895'
            elif year_int > 2025:
                errors['year'] = 'Год не может быть больше 2025'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    # Проверка описания
    description = film.get('description', '')
    if not description:
        errors['description'] = 'Заполните описание'
    elif len(description) > 2000:
        errors['description'] = 'Описание не должно превышать 2000 символов'
    
    if errors:
        return errors, 400
    
    films.append(film)
    new_id = len(films) - 1
    return str(new_id), 201