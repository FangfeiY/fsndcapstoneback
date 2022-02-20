# The Meteor Restaurant App API Backend

## App Overview
TODO

## Live Demo
The API backend is hosted using Heroku at https://themeteor.herokuapp.com/

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
- General manager: <!-- insert token -->
- Staff: <!-- insert token -->

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

<!-- To finish -->
A pre-configured Postman collection, Meteor API, is located at ./postmantest in this project. Import this collection to a Postman workspace and run each folder.

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






