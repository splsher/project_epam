import json
import unittest
from app import app


class TestCreateNews(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        self.headers = {'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
                                         '.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3ODQ4OTQ1MywianRpIjoiMTc4YWFiMDYtNDdlMi00YWRhLWFhNTQtOWFkM2EzMTQ5ZThjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MjMsIm5iZiI6MTY3ODQ4OTQ1MywiZXhwIjoxNjc4NDkwMzUzfQ.tmlwrnofduUIf6WRBw6Dm_1EQTZgXe9DhRuG2kS27kc'}

    def test_create_news_with_valid_data(self):
        data = {
            'title': 'Test News',
            'text': 'This is a test news',
            'photo': 'null'
        }
        response = self.app.post('/wall', headers=self.headers, json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {'message': 'successful operation!'})

    def test_create_news_with_missing_data(self):
        data = {'title': 'Test News'}
        response = self.app.post('/wall', headers=self.headers, json=data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {'error': 'Bad Request'})

    def test_create_news_with_invalid_token(self):
        data = {
            'title': 'Test News',
            'text': 'This is a test news',
            'photo': 'null'
        }
        headers = {'Authorization': 'Bearer invalid_token'}
        response = self.app.post('/wall', headers=headers, json=data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(json.loads(response.data), {'msg': 'Not enough segments'})
