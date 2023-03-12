import json
import unittest
from unittest import mock
from app import app, User, session

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    @mock.patch('models.models.session')
    def test_valid_login(self, mock_session):
        # Mock the User object
        user_mock = mock.MagicMock()
        user_mock.username = 'Tony'
        user_mock.password = '1111'
        user_mock.email = 'tony@gmail.com'
        user_mock.city = 'London'
        user_mock.photo = 'null'

        # Configure the session mock to return the mock user when queried
        mock_session.query.return_value.filter_by.return_value.first.return_value = user_mock

        # Prepare the request data
        auth_data = {'username': 'test_user', 'password': '1111'}
        data = json.dumps(auth_data)

        # Make the request
        response = self.client.post('/login', data=data, content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'token', response.data)

    @mock.patch('models.models.session')
    def test_invalid_login(self, mock_session):
        # Configure the session mock to return None when queried
        mock_session.query.return_value.filter_by.return_value.first.return_value = None

        # Prepare the request data
        auth_data = {'username': 'invaliduser', 'password': 'invalidpassword'}
        data = json.dumps(auth_data)

        # Make the request
        response = self.client.post('/login', data=data, content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User with such username was not found', response.data)