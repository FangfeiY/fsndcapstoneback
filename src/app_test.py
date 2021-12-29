import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, abort

from app import create_app
from models import reset_db, Menu, FoodItem
from env_vars import POSTGRES_USER, POSTGRES_PASS

class MeteorRestaurantTestCase(unittest.TestCase):
    """The unit tests for Meteor Restsurant e-menu and ordering system"""
    
    new_menu_id = None
    new_menu = {
            'name': 'Breakfast Menu',
            'description': 'A variaty of selections that can be too hard to pick just one!'}
    new_fooditem_id = None
    new_fooditem = {
            'name': 'Avocado Toast',
            'description': 'Crunchy wheat bread with creamy avo slices, bacon, and parsley.',
            'price': 10.0,
            'is_vege': False,
            'category': 'Starter'}

    
    def setUp(self):
        """Define test variables and initialize app."""

        self.database_name = "meteor_test"
        self.database_path = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@localhost:5432/{self.database_name}"

        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        # with self.app.app_context():
        #     self.db = SQLAlchemy(self.app)
        #     self.db.drop_all()
        #     self.db.create_all()

        reset_db()

        self.insert_new_menu(self)
        self.insert_new_fooditem(self)

    def tearDown(self):
        pass

    def insert_new_menu(self, test):
        respond = test.client().post('/menus', json=test.new_menu)
        data = json.loads(respond.data)
        test.new_menu_id = data['new_menu']['id']

    def insert_new_fooditem(self, test):
        test.new_fooditem['menu_id'] = test.new_menu_id
        fooditem_respond = test.client().post('/food_items', json=test.new_fooditem)
        fooditem_data = json.loads(fooditem_respond.data)
        test.new_fooditem_id = fooditem_data['new_food_item']['id']

    def test_create_menu_success(self):
        respond = self.client().post('/menus', json=self.new_menu)
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_fooditem_success(self):
        #self.new_fooditem['menu_id'] = self.new_menu_id

        fooditem_respond = self.client().post('/food_items', json=self.new_fooditem)
        fooditem_data = json.loads(fooditem_respond.data)

        self.assertEqual(fooditem_respond.status_code, 200)
        self.assertEqual(fooditem_data['success'], True)

    def test_get_allmenus_success(self):
        respond = self.client().get('/menus')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['menus']))

    def test_get_menubyid_success(self):
        respond = self.client().get(f'/menus/{self.new_menu_id}')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['menu']['id'], self.new_menu_id)
        self.assertTrue(data['menu']['food_items_count'])

    def test_get_fooditembyid_success(self):
        respond = self.client().get(f'/food_items/{self.new_fooditem_id}')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['food_item']['id'], self.new_fooditem_id)

    def test_get_allfooditems_success(self):
        respond = self.client().get('/food_items')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['food_items']))

    def test_get_fooditemsbymenu_success(self):
        respond = self.client().get(f'/menus/{self.new_menu_id}/food_items')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['menu_id'], self.new_menu_id)
        self.assertTrue(len(data['food_items']))

    def test_get_menubyid_invalid_fail(self):
        respond = self.client().get(f'/menus/100')

        self.assertEqual(respond.status_code, 404)

    def test_get_fooditembyid_invalid_fail(self):
        respond = self.client().get(f'/food_items/100')

        self.assertEqual(respond.status_code, 404)

    def test_get_fooditemsbymenu_invalid_fail(self):
        respond = self.client().get(f'/menus/100/food_items')

        self.assertEqual(respond.status_code, 404)

    def test_update_menu_success(self):
        updated_menu = {
            'name': 'Brunch Menu',
            'description': 'Mimosa at your request.',
        }

        respond = self.client().patch(f'/menus/{self.new_menu_id}', json=updated_menu)
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_menu']['name'], updated_menu['name'])

    def test_update_fooditem_success(self):
        updated_fooditem = {
            'menu_id': self.new_menu_id,
            'name': 'Delux Avocado Toast',
            'description': 'Crunchy wheat bread with creamy avo slices, bacon, and parsley.',
            'price': 20,
            'is_vege': False,
            'category': 'Starter'
        }

        respond = self.client().patch(f'/food_items/{self.new_fooditem_id}', json=updated_fooditem)
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_food_item']['name'], updated_fooditem['name'])
    
    def test_del_fooditem_success(self):
        respond = self.client().delete(f'/food_items/{self.new_fooditem_id}')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_food_item_id'], self.new_fooditem_id)

    def test_del_menu_success(self):
        respond = self.client().delete(f'/menus/{self.new_menu_id}')
        data = json.loads(respond.data)

        self.assertEqual(respond.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_menu_id'], self.new_menu_id)    

if __name__ == "__main__":
    print(POSTGRES_USER)
    print(POSTGRES_PASS)

    unittest.main()