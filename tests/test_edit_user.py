import json
from app import app, get_db
from flask_testing import TestCase


class TestEditUser(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        with app.app_context():
            get_db.init_app(app)
            get_db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        with app.app_context():
            get_db.session.remove()
            get_db.drop_all()

    def test_edit_profile_success(self):
        # Create a test user
        test_user = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword',
                     'city': 'Test City', 'photo': 'testphoto'}
        response = self.client.post('/signup', data=json.dumps(test_user), content_type='application/json')

        # Log in as the test user to get a JWT token
        response = self.client.post('/login', data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                                    content_type='application/json')
        token = json.loads(response.data.decode())['access_token']

        # Edit the test user's profile
        new_data = {'username': 'newusername', 'email': 'newemail@example.com', 'password': 'newpassword',
                    'city': 'New City', 'photo': 'newphoto'}
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.put('/edit_profile', data=json.dumps(new_data), headers=headers,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode()), {'message': 'successful operation'})

    def test_edit_profile_missing_token(self):
        # Try to edit a profile without a token
        response = self.client.put('/edit_profile', data=json.dumps({'username': 'newusername'}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 403)
        self.assertEqual(json.loads(response.data.decode()), {'403': 'Access is denied'})

    def test_edit_profile_user_not_found(self):
        # Create a test user and log in to get a JWT token
        test_user = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'testpassword',
                     'city': 'Test City', 'photo': 'testphoto'}
        response = self.client.post('/signup', data=json.dumps(test_user), content_type='application/json')
        response = self.client.post('/login', data=json.dumps({'username': 'testuser', 'password': 'testpassword'}),
                                    content_type='application/json')
        token = json.loads(response.data.decode())['access_token']

        # Try to edit a non-existent user's profile
        new_data = {'username': 'newusername'}
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.put('/edit_profile', data=json.dumps(new_data), headers=headers,
                                   content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode(), 'User not found')

    def test_edit_profile_username_exists(self):
        # Create two test users and log in to get a JWT token
        test_user1 = {'username': 'testuser1', 'email': 'testuser1@example.com', 'password': 'testpassword',
                      'city': 'Test City', 'photo': 'testphoto'}
        response = self.client.post('/signup', data=json.dumps(test_user1), content_type='application/json')
        response = self.client.post('/login', data=json.dumps({'username': '', 'password': ''}))
