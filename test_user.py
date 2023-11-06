import pytest, os, sqlite3, json
from database_test import insert_user, get_users, get_user_by_id, update_user, delete_user
from hello import *


TEST_DB_NAME = "test_database.db"

@pytest.fixture(autouse=True)
def test_db():

    conn = sqlite3.connect(TEST_DB_NAME)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            country TEXT NOT NULL
        );
    ''')
    yield TEST_DB_NAME
    conn.close()
    os.remove(TEST_DB_NAME)  


def test_get_users(test_db):
    users_to_insert = [
        {
            "name": "John Doe the First",
            "email": "johndoe@gmail.com",
            "phone": "1234567890",
            "address": "123 Main St",
            "country": "USA"
        },
        {
            "name": "Jane Smith the Second",
            "email": "janesmith@gmail.com",
            "phone": "9876543210",
            "address": "456 Elm St",
            "country": "Canada"
        },
        {
            "name": "Badi3 Badi3",
            "email": "Badi3@gmail.com",
            "phone": "5555555555",
            "address": "AUB Campus",
            "country": "Lebanon"
        },
    ]

    for user_data in users_to_insert:
        insert_user(user_data)

    retrieved_users = get_users()

    assert len(retrieved_users) == len(users_to_insert)

    for user_data in users_to_insert:
        assert any(user["name"] == user_data["name"] for user in retrieved_users)


def test_insert_user():
    user = {
        "name": "John Doe",
        "email": "jondoe@gmail.com",
        "phone": "067765434567",
        "address": "John Doe Street, Innsbruck",
        "country": "Austria"
    }
    
    inserted_user = insert_user(user)
    
    assert inserted_user["name"] == user["name"]
    assert inserted_user["email"] == user["email"]
    assert inserted_user["phone"] == user["phone"]
    assert inserted_user["address"] == user["address"]
    assert inserted_user["country"] == user["country"]


def test_get_user_by_id():
    user = {
        "name": "John Doe 2",
        "email": "johndoe@gmail.com",
        "phone": "1234567890",
        "address": "123 Main St",
        "country": "USA"
    }
    inserted_user = insert_user(user)
    
    retrieved_user = get_user_by_id(inserted_user["user_id"])
    
    assert retrieved_user["name"] == user["name"]
    assert retrieved_user["email"] == user["email"]
    assert retrieved_user["phone"] == user["phone"]
    assert retrieved_user["address"] == user["address"]
    assert retrieved_user["country"] == user["country"]

def test_update_user():

    user = {
        "name": "John Doe 3",
        "email": "johndoe@gmail.com",
        "phone": "1234567890",
        "address": "123 Main St",
        "country": "USA"
    }
    inserted_user = insert_user(user)
    updated_info = {
        "user_id": inserted_user["user_id"],
        "name": "Updated Name",
        "email": "updatedemail@gmail.com",
        "phone": "9876543210",
        "address": "Updated Address",
        "country": "Lebanon"
    }
    updated_user = update_user(updated_info)
    
    assert updated_user["user_id"] == updated_info["user_id"]
    assert updated_user["name"] == updated_info["name"]
    assert updated_user["email"] == updated_info["email"]
    assert updated_user["phone"] == updated_info["phone"]
    assert updated_user["address"] == updated_info["address"]
    assert updated_user["country"] == updated_info["country"]

def test_delete_user():

    user = {
        "name": "Baba",
        "email": "Baba@gmail.com",
        "phone": "1888822223",
        "address": "Bayte",
        "country": "Lebanon"
    }
    inserted_user = insert_user(user)
    
    deletion_message = delete_user(inserted_user["user_id"])
    
    assert deletion_message["status"] == "User deleted successfully"



@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_api_get_user(client, test_db):
    response = client.get('/api/users/1')  # Replace '1' with the user_id you want to test
    assert response.status_code == 200 
    data = json.loads(response.get_data(as_text=True))
    

def test_api_add_user(client, test_db):
    user_data = {
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": "1234567890",
        "address": "123 Main St",
        "country": "USA"
    }
    response = client.post('/api/users/add', json=user_data)
    assert response.status_code == 200 
    data = json.loads(response.get_data(as_text=True))
    user_data_with_ID = {
        "user_id" : data["user_id"],
        "name": "John Doe",
        "email": "johndoe@gmail.com",
        "phone": "1234567890",
        "address": "123 Main St",
        "country": "USA"
    }
    assert data == user_data_with_ID


def test_api_update_user(client, test_db):
    updated_user_data = {
        "user_id": 1,  # Replace '1' with the actual user_id you want to update
        "name": "Updated Name",
        "email": "updatedemail@gmail.com",
        "phone": "9876543210",
        "address": "Updated Address",
        "country": "Lebanon"
    }
    response = client.put('/api/users/update', json=updated_user_data)
    assert response.status_code == 200  
    data = json.loads(response.get_data(as_text=True))


def test_api_delete_user(client, test_db):
    user_id_to_delete = 1  
    response = client.delete(f'/api/users/delete/{user_id_to_delete}')
    assert response.status_code == 200  
    data = json.loads(response.get_data(as_text=True))