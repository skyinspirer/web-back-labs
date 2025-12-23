from flask import Blueprint, render_template, request, jsonify, session, redirect
from db import db
from db.models import gift_box
from flask_login import current_user, login_required
import random

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def main():
    boxes = gift_box.query.all()
    unopened_count = gift_box.query.filter_by(is_opened=False).count()
    opened_in_session = len(session.get('opened_boxes', []))
    
    return render_template('lab9/index.html',
                           boxes=boxes,
                           unopened_count=unopened_count,
                           opened_in_session=opened_in_session)

@lab9.route('/lab9/open_box', methods=['POST'])
def open_box():
    box_id = request.json.get('box_id')
    box = gift_box.query.get(box_id)
    
    if not box:
        return jsonify({'error': 'Коробка не найдена'}), 404
    
    if box.auth_required and not current_user.is_authenticated:
        return jsonify({'auth_needed': True})
    
    if box.is_opened:
        return jsonify({'already_opened': True})
    
    if 'opened_boxes' not in session:
        session['opened_boxes'] = []
    
    if len(session['opened_boxes']) >= 3:
        return jsonify({'limit_exceeded': True})
    
    box.is_opened = True
    db.session.commit()
    
    session['opened_boxes'] = session['opened_boxes'] + [box_id]
    
    return jsonify({
        'success': True,
        'redirect_url': f'/lab9/congratulation/{box_id}'
    })

@lab9.route('/lab9/reset_boxes', methods=['POST'])
@login_required
def reset_boxes():
    boxes = gift_box.query.all()
    for box in boxes:
        box.is_opened = False
    
    session['opened_boxes'] = []
    
    for box in boxes:
        box.pos_top = random.randint(50, 500)
        box.pos_left = random.randint(50, 900)
    
    db.session.commit()
    return jsonify({'success': True})

@lab9.route('/lab9/congratulation/<int:box_id>')
def congratulation(box_id):
    box = gift_box.query.get(box_id)
    if not box or not box.is_opened:
        return redirect('/lab9/')
    
    gift_id = box_id + 10
    img_path = f'/static/lab9/{gift_id}.jpg'
    
    return render_template('lab9/congratulation.html',
                           box=box,
                           img_path=img_path,
                           box_id=box_id)