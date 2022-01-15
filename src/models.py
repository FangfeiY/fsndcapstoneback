import json
import os
from sqlalchemy import Column, String, Integer, Float, Boolean, create_engine
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from src.env_vars import DATABASE_URL

# app = Flask("app")
# app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)

db = SQLAlchemy()

def setup_db(app):
    db.app = app
    db.init_app(app)

'''
reset_db()
    To set up tables in data base, call this function from command line on app's first run,
    after importing app.py and models.py
'''
def reset_db():
    db.drop_all()
    db.create_all()

'''
FoodItem
'''
class FoodItem(db.Model):
    __tablename__ = 'food_items'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, db.ForeignKey('menus.id'), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    is_vege = Column(Boolean, nullable=False)
    category = Column(String, nullable=False)

    def __init__(self, menu_id, name, description, price, is_vege, category):
        self.menu_id = menu_id
        self.name = name
        self.description = description
        self.price = price
        self.is_vege = is_vege
        self.category = category
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return{
            'id': self.id,
            'menu_id': self.menu_id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'is_vege': self.is_vege,
            'category': self.category
        }

    def __repr__(self):
        return json.dumps(self.format())

'''
Menu

'''
class Menu(db.Model):  
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    food_items = db.relationship('FoodItem', backref='parent_menu', lazy=True, cascade='all, delete-orphan')

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_short(self):
        return {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'food_items_count': len(self.food_items)
        }

    def format_long(self):
        return {
        'id': self.id,
        'name': self.name,
        'description': self.description,
        'food_items': self.food_items
        }
    
    def __repr__(self):
        return json.dumps(self.format_long())

    @classmethod
    def get_all_long(cls):
        menus = Menu.query.order_by(Menu.id).all()

        return [menu.format_long() for menu in menus]

    @classmethod
    def get_all_short(cls):
        menus = Menu.query.order_by(Menu.id).all()

        return [menu.format_short() for menu in menus]