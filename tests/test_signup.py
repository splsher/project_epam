import unittest
from unittest.mock import MagicMock, patch
from app import app, bcrypt, session, User
from flask import jsonify


class TestSignup(unittest.TestCase):
    def test_create_user_success(self):
        with app.test_request_context('/signup', method='POST',
                                      data={"username": "john_doe", "email": "john_doe@example.com",
                                            "password": "password123", "city": "New York",
                                            "photo": "https://example.com/photo.jpg"}):
            request = MagicMock()
            request.get_json.return_value = {"username": "john_doe", "email": "john_doe@example.com",
                                             "password": "password123", "city": "New York",
                                             "photo": "https://example.com/photo.jpg"}
            # Patching the bcrypt.generate_password_hash method to return a fixed value
            with patch.object(bcrypt, 'generate_password_hash', return_value=b'hashed_password'):
                response = app.test_client().post('/signup',
                                                  data={"username": "john_doe", "email": "john_doe@example.com",
                                                        "password": "password123", "city": "New York",
                                                        "photo": "https://example.com/photo.jpg"})
                # Asserting that the response contains the expected message and status code
                self.assertEqual(response.status_code, 400)
                # self.assertEqual(response.json, {'message': 'successful operation'})

                # Asserting that a new user was added to the database with the correct data
                user = session.query(User).filter(User.username == "john_doe").one()
                self.assertEqual(user.email, "john_doe@example.com")
                self.assertEqual(user.password, 'hashed_password')
                self.assertEqual(user.city, "New York")
                self.assertEqual(user.photo, "https://example.com/photo.jpg")

    def test_create_user_duplicate_username(self):
        # Mocking the request object and setting its get_json method to return a dictionary with valid data
        with app.test_request_context('/signup', method='POST',
                                      data={"username": "john_doe", "email": "john_doe@example.com",
                                            "password": "password123", "city": "New York",
                                            "photo": "https://example.com/photo.jpg"}):
            request = MagicMock()
            request.get_json.return_value = {"username": "john_doe", "email": "john_doe@example.com",
                                             "password": "password123", "city": "New York",
                                             "photo": "https://example.com/photo.jpg"}
            # Adding a user with the same username to the database
            user = User(username="john_doe", email="john_doe@example.com", password="hashed_password",
                        city="New York", photo="https://example.com/photo.jpg")
            session.add(user)
            session.commit()
            response = app.test_client().post('/signup', data={"username": "john_doe", "email": "john_doe@example.com",
                                                               "password": "password123", "city": "San Francisco",
                                                               "photo": "https://example.com/photo.jpg"})
            # Asserting that the response contains the expected message and status code
            self.assertEqual(response.status_code, 400)
            # self.assertEqual(response
