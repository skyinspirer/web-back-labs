from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from flask_login import current_user, login_required
import random
import json
import os
import math

lab9 = Blueprint('lab9', __name__)

# Конфигурация коробок
BOXES_CONFIG = [
    {"id": 1, "message": "Поздравляем! Вы нашли сладкий подарок!", "auth_required": False},
    {"id": 2, "message": "Ура! Вы выиграли новогодний календарь!", "auth_required": False},
    {"id": 3, "message": "Поздравляем с открытием! Волшебный момент!", "auth_required": True},
    {"id": 4, "message": "Вы нашли праздничное настроение!", "auth_required": False},
    {"id": 5, "message": "Поздравляем! Новогоднее чудо случилось!", "auth_required": False},
    {"id": 6, "message": "Ура! Вы нашли зимнюю сказку!", "auth_required": True},
    {"id": 7, "message": "Поздравляем! Волшебный подарок ваш!", "auth_required": False},
    {"id": 8, "message": "Вы открыли коробку с праздником!", "auth_required": False},
    {"id": 9, "message": "Поздравляем! Новогоднее волшебство!", "auth_required": True},
    {"id": 10, "message": "Ура! Главный приз года!", "auth_required": False},
]

# Размеры коробки 
BOX_WIDTH = 120   
BOX_HEIGHT = 150  
MIN_DISTANCE = 140  

def is_position_valid(new_pos, existing_positions):
    
    if not existing_positions:
        return True
    # Проверяет расстояние между коробками
    for pos in existing_positions:
        # Вычисляем расстояние между центрами
        distance = math.sqrt(
            (new_pos['left'] - pos['left']) ** 2 +
            (new_pos['top'] - pos['top']) ** 2
        )
        
        # Если расстояние меньше минимального - позиция невалидна
        if distance < MIN_DISTANCE:
            return False
    
    return True

def generate_unique_position(existing_positions, max_attempts=100):
    
    # Размеры контейнера
    container_width = 1400
    container_height = 650
    
    # Учитываем размеры коробки при расчете границ
    margin = 30
    max_left = container_width - BOX_WIDTH - margin
    max_top = container_height - BOX_HEIGHT - margin
    
    for attempt in range(max_attempts):
        # Генерируем случайную позицию
        pos_top = random.randint(margin, max_top)
        pos_left = random.randint(margin, max_left)
        
        new_pos = {'top': pos_top, 'left': pos_left}
        
        # Проверяем на наложение
        if is_position_valid(new_pos, existing_positions):
            return new_pos
    

    print(f"Внимание: не удалось найти уникальную позицию после {max_attempts} попыток")
    return {
        'top': random.randint(margin, max_top),
        'left': random.randint(margin, max_left)
    }

def init_session_data():

    if 'lab9_boxes' not in session:
        boxes_data = []
        existing_positions = []
        
        for box in BOXES_CONFIG:
            # Генерируем уникальную позицию
            position = generate_unique_position(existing_positions)
            
            boxes_data.append({
                'id': box['id'],
                'is_opened': False,
                'pos_top': position['top'],
                'pos_left': position['left'],
                'auth_required': box['auth_required'],
                'message': box['message']
            })
            
            # Добавляем позицию в список существующих
            existing_positions.append(position)
        
        session['lab9_boxes'] = json.dumps(boxes_data)
    
    if 'lab9_opened_boxes' not in session:
        session['lab9_opened_boxes'] = json.dumps([])

def get_boxes():

    init_session_data()
    return json.loads(session['lab9_boxes'])

def get_opened_boxes():

    init_session_data()
    return json.loads(session['lab9_opened_boxes'])

def save_boxes(boxes):

    session['lab9_boxes'] = json.dumps(boxes)

def save_opened_boxes(opened_boxes):

    session['lab9_opened_boxes'] = json.dumps(opened_boxes)

@lab9.route('/lab9/')
def main():
    init_session_data()
    
    boxes = get_boxes()
    opened_boxes = get_opened_boxes()
    
    # Обновляем статус открытых коробок
    for box in boxes:
        box['is_opened'] = box['id'] in opened_boxes
    
    # Логируем позиции для отладки
    print("Текущие позиции коробок:")
    for box in boxes:
        print(f"Коробка {box['id']}: top={box['pos_top']}, left={box['pos_left']}")
    
    unopened_count = len([box for box in boxes if not box['is_opened']])
    
    return render_template('lab9/index.html',
                           boxes=boxes,
                           unopened_count=unopened_count,
                           opened_in_session=len(opened_boxes))

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    try:
        box_id = int(request.json.get('box_id'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Некорректный ID коробки'}), 400
    
    boxes = get_boxes()
    opened_boxes = get_opened_boxes()
    
    # Находим коробку
    box = next((b for b in boxes if b['id'] == box_id), None)
    
    if not box:
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    # Проверка авторизации
    if box['auth_required'] and not current_user.is_authenticated:
        return jsonify({'auth_needed': True})
    
    # Проверка на уже открытую коробку
    if box['id'] in opened_boxes:
        return jsonify({'already_opened': True})
    
    # Проверка лимита (максимум 3 коробки)
    if len(opened_boxes) >= 3:
        return jsonify({'limit_exceeded': True})
    
    # Добавляем коробку в список открытых
    opened_boxes.append(box_id)
    save_opened_boxes(opened_boxes)
    
    # Помечаем коробку как открытую в основном списке
    for b in boxes:
        if b['id'] == box_id:
            b['is_opened'] = True
    save_boxes(boxes)
    
    return jsonify({
        'success': True,
        'redirect_url': url_for('lab9.congratulation', box_id=box_id)
    })

@lab9.route('/lab9/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():

    boxes = []
    existing_positions = []
    
    for box_config in BOXES_CONFIG:
        # Генерируем уникальную позицию
        position = generate_unique_position(existing_positions)
        
        boxes.append({
            'id': box_config['id'],
            'is_opened': False,
            'pos_top': position['top'],
            'pos_left': position['left'],
            'auth_required': box_config['auth_required'],
            'message': box_config['message']
        })
        
        # Добавляем позицию в список существующих
        existing_positions.append(position)
    
    save_boxes(boxes)
    save_opened_boxes([])
    
    # Логируем новые позиции
    print("Новые позиции после сброса:")
    for box in boxes:
        print(f"Коробка {box['id']}: top={box['pos_top']}, left={box['pos_left']}")
    
    return jsonify({'success': True})

@lab9.route('/lab9/congratulation/<int:box_id>')
def congratulation(box_id):
    boxes = get_boxes()
    opened_boxes = get_opened_boxes()
    
    # Проверяем, что коробка существует и открыта
    box = next((b for b in boxes if b['id'] == box_id), None)
    
    if not box or box_id not in opened_boxes:
        return redirect(url_for('lab9.main'))
    
    # Используем gift11-gift20 для содержимого
    gift_number = box_id + 10
    img_path = f'/static/lab9/gift{gift_number}.jpg'
    
    # Проверяем существование файла
    if not os.path.exists(f'static/lab9/gift{gift_number}.jpg'):
        img_path = '/static/lab9/default_gift.jpg'
    
    return render_template('lab9/congratulation.html',
                           box=box,
                           img_path=img_path,
                           box_id=box_id)


@lab9.route('/lab9/debug_clear')
def debug_clear():

    session.pop('lab9_boxes', None)
    session.pop('lab9_opened_boxes', None)
    return redirect(url_for('lab9.main'))

@lab9.route('/lab9/debug_positions')
def debug_positions():

    boxes = get_boxes()
    
    # Проверяем наложение
    positions = []
    overlaps = []
    
    for i, box1 in enumerate(boxes):
        for j, box2 in enumerate(boxes):
            if i >= j:  
                continue
            

            distance = math.sqrt(
                (box1['pos_left'] - box2['pos_left']) ** 2 +
                (box1['pos_top'] - box2['pos_top']) ** 2
            )
            
            if distance < MIN_DISTANCE:
                overlaps.append({
                    'box1': box1['id'],
                    'box2': box2['id'],
                    'distance': round(distance, 1)
                })
    
    return jsonify({
        'boxes': boxes,
        'overlaps': overlaps,
        'min_distance': MIN_DISTANCE,
        'box_width': BOX_WIDTH,
        'box_height': BOX_HEIGHT
    })