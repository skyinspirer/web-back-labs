from . import db
from flask_login import UserMixin
from datetime import datetime

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login = db.Column(db.String(30), nullable = False, unique = True)
    password = db.Column(db.String(162), nullable = False)

class articles(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable = False)
    article_text = db.Column(db.Text, nullable = False)
    is_favorite = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)

# Новые модели для онлайн-магазина мебели
class Product(db.Model):
    __tablename__ = 'rgz_products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    image_url = db.Column(db.String(200))
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'image_url': self.image_url,
            'stock': self.stock
        }

class CartItem(db.Model):
    __tablename__ = 'rgz_cart_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('rgz_products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('users', backref=db.backref('rgz_cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('rgz_cart_items', lazy=True))

class Order(db.Model):
    __tablename__ = 'rgz_orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('users', backref=db.backref('rgz_orders', lazy=True))

class OrderItem(db.Model):
    __tablename__ = 'rgz_order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('rgz_orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('rgz_products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)
    
    order = db.relationship('Order', backref=db.backref('rgz_items', lazy=True))
    product = db.relationship('Product')