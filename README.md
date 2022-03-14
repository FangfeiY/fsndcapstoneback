# The Meteor Restaurant App API Backend

## App Overview
Welcome to the API backend of the e-menu app for the imaginary Meteor restaurant! 

The app is desigened serve types of audiences: restaurant manager and staff. Operations they are allowed to do are described below.

## Live Demo
The API backend is hosted using Heroku at https://themeteor.herokuapp.com/

## Database Design
There are two entities in the app - Menu and Food Item. They are in one-to-many relation. One menu can contain many food items, and one food item can only belong to one menu. 

- Example of menu: {"id": 1, "name": "Breakfest Menu", "description": "Wake up your morning with a great test", "food_items": [1]}
- Example of food item: {"id": 1, "menu_id": 1, "name": "Avocado toast", "description": "Avo, Ancient Grain Toast, Black Pepper, Beacon", "price": 6.0, "is_vege": False, "category": "Flatbread"}

![image](https://github.com/FangfeiY/fsndcapstoneback/blob/master/readmeContent/Entities.PNG)

## RBAC
The API endpoint implements RBAC. There are two roles provisioned for this app: General Manager and Staff. Below lists their permissions to the endpoints and operations.

| Role            | Permissions                                     |
|-----------------|-------------------------------------------------|
| General Manager | ADD menu; UPDATE menu; DELETE menu; VIEW menus; |
|		          | ADD food item; UPDATE food item; 		        |
|                 | DELETE food item; VIEW food items;		        |
| Staff           | VIEW menus;					                    |
|                 | UPDATE food item; VIEW food item;               |

## Authentication
Since the RBAC, the API endpoint is access controlled. Clients need to register at app's authentication service, pass authentication, and get access token before they can successfully use the endpoint. 

This app use Auth0 as authentication service provider. Below is its signature.
- App domain: calaveras.us.auth0.com
- Client ID: dnSQtZc1mn8s3n9lA6D3jpMjsl0s6pzT
- Client secret: QjS0xeQukpRGucV-QqroLT_mWHjtBzAk2m5izz_LeQ7tofwaGdvVF1k7jYzLSC_a

Usually new user should go to this app's auth portal using the link below to register and get token. 

```
https://calaveras.us.auth0.com/authorize?audience=meteor&response_type=token&client_id=dnSQtZc1mn8s3n9lA6D3jpMjsl0s6pzT&redirect_uri=https://themeteor.herokuapp.com/login-results
```

But since this is a course demo project, to allow reviewers to easilily test teh API, I've pre-configured two users for testing, once for each role. Below lists their tokens:
- General manager: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFvaGp1NDZLSGdjakR4eE9IdW9YdSJ9.eyJpc3MiOiJodHRwczovL2NhbGF2ZXJhcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBhNDgwNzQ1ZjA5MWQwMDY5OTUwYzk0IiwiYXVkIjoibWV0ZW9yIiwiaWF0IjoxNjQ3MjI3NzQ1LCJleHAiOjE2NDczMTM3NDUsImF6cCI6ImRuU1F0WmMxbW44czNuOWxBNkQzanBNanNsMHM2cHpUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Zm9vZGl0ZW1zIiwiZGVsZXRlOm1lbnVzIiwiZ2V0OmZvb2RpdGVtcyIsImdldDptZW51cyIsInBhdGNoOmZvb2RpdGVtcyIsInBhdGNoOm1lbnVzIiwicG9zdDpmb29kaXRlbXMiLCJwb3N0Om1lbnVzIl19.SfqnkFB3V84YZzy-EDGc21i-h0H6olwrtGFcCQIGvUbzgGpFl1H4dPZVxVfg1uUhUCQuT6Wwc-RM_HSa2Mt37Zrgcclp8NZHbtTNUOqZYXdLIqgZ7qOACg5F9nJY9NQbk5rs_azjBnpZWGwPRbwPd7Fqaw2ez_jjK3rlX6cHFxMWIVy2rBmsbQj9-aIjUcUx7yU5Dp0Tq0uCz7GiRpdKF2Ln-7oiO6TIYurupEA05WdsafMwls3vdn1oci8ziC5-Y6OzLWDRfmVo71ll2D9tyJAIedUV8e8hMyf1fKdFca3XHxB2MSnD2wawPMg1PDIE2Q44FgkMtY6slvG0PMJH0A
- Staff: eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFvaGp1NDZLSGdjakR4eE9IdW9YdSJ9.eyJpc3MiOiJodHRwczovL2NhbGF2ZXJhcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjBkZDJiOWI3YWU5YTYwMDY5ZjIxYmJmIiwiYXVkIjoibWV0ZW9yIiwiaWF0IjoxNjQ3MjI4MDk0LCJleHAiOjE2NDczMTQwOTQsImF6cCI6ImRuU1F0WmMxbW44czNuOWxBNkQzanBNanNsMHM2cHpUIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6Zm9vZGl0ZW1zIiwiZ2V0Om1lbnVzIiwicGF0Y2g6Zm9vZGl0ZW1zIl19.LLMaE2BOCQE1DPfIL2pE2UONZH2whXcewo-0zfwXWUUoWlFNSh4HlFMspWlU2bLGCxJeJ0_21c1SalpnQAhH651XbZ-7zMokEcJribbMmPZwVOBsfdYLoce5e_wgE2TkQ12hx9K9Ym7TaB7tYVYqjeJ0PG-SCPULSThRW0IXRMhnCPitEYzkmMfgukrzqaIjUkLPJ80B2tfrfNkrc7W0aTTkQR0c1JODkM1G_lO6ZRqXXksjwE7GIYtsU56eFMhfrZ1z3BSZwF1WoT5HxCxQ4KbgSLj3yChuvnnWi2ufJlU-69d2rdR7tLr2boAeJzODf0GDSmczOwUmzpH0MpTRzA

## Local Setup
### Set Up Environment Vars
In a terminal, switch to backend folder and run the following.
```
env_config
```

### Create Python Virtual Environment
```
python3 venv env
.\env\Scripts\activate
```

### Install Required Packages
```
pip3 install -r requirements.txt
```

### Set Up Local Database for Dev
In another terminal, open a psql session to access local Postgres service:
```
psql "postgresql://<username>:<password>@localhost:5432"

#Create a database called meteor:
CREATE DATABASE meteor;
```

In the virtual env terminal, run a databse migration to set up tables needed for this app:
```
flask db upgrade, OR
python3 manage.py db upgrade
```

## Testing
### Unit Test
Unit test cases are written in the file ./src/app_test.py. To run the unit tests, switch to the src folder in the virtual env terminal and run:
```
python3 app_test.py
```
For testing purpose, the app is designed to ignore authentication for unit test.

### Postman Test
Postman test can be used for:
- Verifying the API endpoints at https://themeteor.herokuapp.com/ are working.
- Testing RBAC with local app server and database.

A pre-configured Postman collection, Meteor API, is located at ./postmantest in this project. Import this collection to a Postman workspace and run each folder. Restaurant manager and staff tokens are stored in collection's variables.

To switch between production app and local test app, modify the {{host}} variable of the Meteor API collection:
- To veirify production app, set {{host}} = https://themeteor.herokuapp.com/.
- To test locally, set {{host}} = http://127.0.0.1.

### Test Data
If needed, the file ./src/postman_test.py can be used to insert sample data to the local database.
```
python3 postman_test.py
```

## API Doc
See the documentation in the Postman collection: Meteor API collection -> three dots button -> View documentation.






