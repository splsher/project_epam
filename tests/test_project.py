import pytest
from flask import Flask, jsonify, render_template

from models.models import Wall


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'mysecretkey'
    return app


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    client = app.test_client()
    return client


def test_my_route(client):
    response = client.post('/')
    assert response.status_code == 404


def test_edit_profile(client):
    data = {'username': 'new_username'}
    response = client.put('/edit_profile', json=data)
    assert response.status_code == 404
    # assert that the user's profile has been updated with the new username


import unittest
from flask import Flask, request, json
from app import app, auth, create_access_token, session, User

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_valid_login(self):
        with self.app as client:
            # Create a test user
            user = User(username='test_user', password='1111', email='test_email@gmail.com', city='test_city', photo='null')
            session.add(user)
            session.commit()

            # Prepare the request data
            auth_data = {'username': 'test_user', 'password': '1111', 'email': 'test_email@gmail.com', 'city': 'test_city',
                         'photo': 'null'}
            data = json.dumps(auth_data)

            # Make the request
            response = client.post('/login', data=data, content_type='application/json')

            # Check the response
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'token', response.data)

    def test_invalid_login(self):
        with self.app as client:
            # Prepare the request data
            auth_data = {'username': 'invaliduser', 'password': 'invalidpassword'}
            data = json.dumps(auth_data)

            # Make the request
            response = client.post('/login', data=data, content_type='application/json')

            # Check the response
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'User with such username was not found', response.data)



