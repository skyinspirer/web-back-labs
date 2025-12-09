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
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    
    if film['title'] == '':
        film['title'] = film['title_ru']

    films[id] = film
    return films[id]


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    
    if film['title'] == '':
        film['title'] = film['title_ru']
    
    films.append(film)
    new_id = len(films) -1
    return str(new_id), 201