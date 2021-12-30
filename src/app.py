'''
Entry to start the flask app
Synopsis: python app.py <db_name>. DB with the name has to exist in the Postgres server before running the app
Example: "python app.py meteor", or "python app.py meteor_test"
'''

import os
import sys
import json
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from sqlalchemy import exc

from src.models import setup_db, FoodItem, Menu
from src.auth import AuthError, requires_auth
from src.env_vars import DATABASE_URL

def set_endpoints(app):
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def index():
        return 'Welcome to Meteor Restaurant and Bar!'

    @app.route('/login-results')
    def login_results():
        return 'Welcome to Meteor Restaurant and Bar! You are successfully logged in!'

    @app.route('/login')
    def login():
        return "Please login to Meteor Restaurant's menu system!"
    
    @app.route('/logout')
    def logout():
        return "You are now logged out from Meteor Restaurant's menu system!"

    '''@TODO: CRUD for menus'''

    @app.route('/menus')
    @requires_auth('get:menus')
    def get_all_menus():
        try:
            menu_format = request.args.get('format')

            if menu_format == 'long':
                menu = Menu.get_all_long()
            else:
                menu = Menu.get_all_short()

            return jsonify({
                'success': True,
                'menus': menu
            }), 200
        except:
            abort(500)

    @app.route('/menus/<int:menu_id>')
    @requires_auth('get:menus')
    def get_menu_by_id(menu_id):
        menu = Menu.query.filter(Menu.id == menu_id).one_or_none()

        if menu is None: abort(404)

        return jsonify({
            'success': True,
            'menu': menu.format_short()
        }), 200

    @app.route('/menus', methods=['POST'])
    @requires_auth('post:menus')
    def create_menu():
        try:
            body = request.get_json()

            new_menu = Menu(
                name = body.get('name', ''),
                description = body.get('description', None)
            )
            new_menu.insert()

            return jsonify({
                'success': True,
                'new_menu': new_menu.format_short()
            }), 200
        except:
            abort(500)

    @app.route('/menus/<int:menu_id>', methods=['PATCH'])
    @requires_auth('patch:menus')
    def update_menu(menu_id):
        try:
            menu = Menu.query.filter(Menu.id == menu_id).one_or_none()

            if menu is None: abort(404)
            
            body = request.get_json()

            new_name = body.get('name', None)
            new_description = body.get('description', None)

            if new_name is not None: menu.name = new_name
            if new_description is not None: menu.description = new_description

            menu.update()

            return jsonify({
                'success': True,
                'updated_menu': menu.format_short()
            }), 200
        except:
            abort(500)

    @app.route('/menus/<int:menu_id>', methods=['DELETE'])
    @requires_auth('delete:menus')
    def delete_menu(menu_id):
        try:
            menu = Menu.query.filter(Menu.id == menu_id).one_or_none()

            if menu is None: abort(404)
            
            menu.delete()

            return jsonify({
                'success': True,
                'deleted_menu_id': menu_id
            }), 200
        except:
            abort(500)

    '''@TODO: CRUD for food items'''

    @app.route('/food_items/<int:food_item_id>')
    @requires_auth('get:fooditems')
    def get_fooditem_by_id(food_item_id):
        food_item = FoodItem.query.filter(FoodItem.id == food_item_id).one_or_none()

        if food_item is None: abort(404)

        return jsonify({
            'success': True,
            'food_item': food_item.format()
        }), 200

    @app.route('/food_items')
    @requires_auth('get:fooditems')
    def get_all_fooditems():
        try:
            food_items = FoodItem.query.order_by(FoodItem.id).all()

            return jsonify({
                'success': True,
                'food_items': [item.format() for item in food_items]
            }), 200
        except:
            abort(500)

    @app.route('/menus/<int:menu_id>/food_items')
    @requires_auth('get:fooditems')
    def get_fooditems_by_menu(menu_id):
        menu = Menu.query.filter(Menu.id == menu_id).one_or_none()

        if menu is None: abort(404)

        return jsonify({
            'success': True,
            'menu_id': menu.id,
            'menu_name': menu.name,
            'menu_description': menu.description,
            'food_items': [item.format() for item in menu.food_items]
        }), 200

    @app.route('/food_items', methods=['POST'])
    @requires_auth('post:fooditems')
    def create_fooditem():
        try:
            body = request.get_json()

            new_food_item = FoodItem(
                menu_id = body.get('menu_id', 0),
                name = body.get('name', 'sample food item'),
                description = body.get('description', None),
                price = body.get('price', 0),
                is_vege = body.get('is_vege', False),
                category = body.get('category', 'sample food category')
            )

            new_food_item.insert()

            return jsonify({
                'success': True,
                'new_food_item': new_food_item.format()
            }), 200
        except:
            abort(500)

    @app.route('/food_items/<int:food_item_id>', methods=['PATCH'])
    @requires_auth('patch:fooditems')
    def update_fooditem(food_item_id):
        try:
            food_item = FoodItem.query.filter(FoodItem.id == food_item_id).one_or_none()

            if food_item is None: abort(404)
            
            body = request.get_json()

            new_menu_id = body.get('menu_id', None)
            new_name = body.get('name', None)
            new_description = body.get('description', None)
            new_price = body.get('price', None)
            new_is_vege = body.get('is_vege', None)
            new_category = body.get('category', None)

            if new_menu_id is not None: food_item.menu_id = new_menu_id
            if new_name is not None: food_item.name = new_name
            if new_description is not None: food_item.description = new_description
            if new_price is not None: food_item.price = new_price
            if new_is_vege is not None: food_item.is_vege = new_is_vege
            if new_category is not None: food_item.category = new_category

            food_item.update()

            return jsonify({
                'success': True,
                'updated_food_item': food_item.format()
            }), 200
        except:
            abort(500)

    @app.route('/food_items/<int:food_item_id>', methods=['DELETE'])
    @requires_auth('delete:fooditems')
    def delete_fooditem(food_item_id):
        try:
            food_item = FoodItem.query.filter(FoodItem.id == food_item_id).one_or_none()

            if food_item is None: abort(404)
            
            food_item.delete()

            return jsonify({
                'success': True,
                'deleted_food_item_id': food_item_id
            }), 200
        except:
            abort(500)

    '''Error handlers'''
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'internal server error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(auth_error):
        err_code = auth_error.error['code']
        err_descrip = auth_error.error['description']
        message = f'{err_code}: {err_descrip}'
        print(message)

        return jsonify({
            'success': False,
            'error': auth_error.status_code,
            'message': message
        }), auth_error.status_code


def create_app(db_uri):
    app = Flask("app")
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    setup_db(app)
    
    CORS(app, resources={r"/*": {"origins": "*"}})
    set_endpoints(app)

    return app

# if __name__ == '__main__':
    # if(len(sys.argv) < 2):
    #     print("Please provide database name as 1st argument to this script.")
    # else:
    #     db_name = sys.argv[1]
    #     app = create_app(db_name)
    #     app.run()

app = create_app(DATABASE_URL)

if __name__ == '__main__':
    app.run()