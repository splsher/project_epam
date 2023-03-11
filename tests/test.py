import pytest
from models.models import User
from app import create_user, get_db


@pytest.fixture()  # decorative
def app():
    app = create_user()

    with app.data():
        get_db.create_all

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

# def test_new_user():
#     user = User()
#     assert user.username == 'Potap'
#     assert user.email == 'buenos@gmail.com'
#
#     assert user.hashed_password != 'FlaskIsAwesome'
#     assert user.city == 'Lviv'
#     assert user.photo == 'null'
