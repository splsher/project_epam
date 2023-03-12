import json
import unittest
from unittest.mock import patch, MagicMock

from app import app


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    @patch('app.session')
    def test_login_success(self, mock_session):
        mock_query = MagicMock()
        mock_query.filter().all.return_value = [MagicMock(id=1)]
        mock_session.query.return_value = mock_query

        response = self.app.post('/login', data=json.dumps({'username': 'testuser'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json)
        self.assertIsInstance(response.json['token'], str)

    @patch('app.session')
    def test_login_user_not_found(self, mock_session):
        mock_query = MagicMock()
        mock_query.filter().all.return_value = []
        mock_session.query.return_value = mock_query

        response = self.app.post('/login', data=json.dumps({'username': 'testuser'}),
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'User with such username was not found')

