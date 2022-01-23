'''
This script sets up mock data in the test database for Postman tests.
Run this script to start the flask app for Postman testing.

Example: python postman_test.py
Pre-requisite: create a database named "meteor_test" in local Postges server
'''

import os
from src.app import create_app
from src.models import db, reset_db, FoodItem, Menu
from src.env_vars import POSTGRES_USER, POSTGRES_PASS

def insert_menus():
    count = 5
    for i in range(count):
        menu = Menu(name=f'Menu { i + 1 }', description=f'Menu description { i + 1 }')
        db.session.add(menu)

    db.session.commit()

def insert_fooditems():
    count = 5
    categories = ['Appetizer', 'Entre']

    for i in range(count):
        fooditem = FoodItem(
                menu_id = 1,
                name = f'Food item { i + 1 }',
                description = f'Food item description { i + 1 }',
                price = i/(i+1) * 10,
                is_vege = False,
                category = categories[i%2]
        )
        db.session.add(fooditem)
    
    db.session.commit()

'''
Run this function to reset the data before moving to test another folder
'''
def set_test_data():
    try:
        insert_menus()
        insert_fooditems()
    except:
        db.session.rollback()
        raise

if __name__ == '__main__':
    db_uri = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@localhost:5432/meteor"

    meteor_app = create_app(db_uri)

    reset_db()

    set_test_data()
    
    meteor_app.run()
    
