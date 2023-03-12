# import unittest
#
# from app import app
# from tests.test_project import TestLogin
# from models.models import Wall, session
#
# test_instance = TestLogin()
# test_instance.test_valid_login()
#
#
# class TestLogin(unittest.TestCase):
#     def setUp(self):
#         self.app = app.test_client()
#
#
# def test_delete_news(self, jwt_token):
#     # create test news
#     news = Wall(title='Test News', content='Test Content', author='Test Author')
#     session.add(news)
#     session.commit()
#
#     # send delete request with JWT token
#     response = self.delete('/delete_news', headers={'Authorization': f'Bearer {jwt_token}'})
#
#     # check response status and message
#     assert response.status_code == 200
#     assert response.json == {'message': 'successful operation'}
#
#     # check if news was deleted
#     assert session.query(Wall).filter_by(title='Test News').first() is None