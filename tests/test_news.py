from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token

app = Flask(__name__, template_folder='templates', static_folder='static')
from models.models import User
import pytest

jwt = JWTManager(app)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture
def jwt_token():
    engine = create_engine('mysql+pymysql://root:Bonia9977@localhost/social_network')
    Session = sessionmaker(bind=engine)
    session = Session()

    # create test user
    user = User(username='tester', email='tester@example.com', password='test123', city='test city', photo='test.png')
    session.add(user)
    session.commit()

    # generate JWT token for test user
    access_token = create_access_token(identity=user.id)
    yield access_token

    # clean up test user from database
    session.delete(user)
    session.commit()


def test_display_news(client, jwt_token):
    response = client.get('/news', headers={'Authorization': 'Bearer ' + jwt_token})
    assert response.status_code == 200
    assert len(response.json) == 0
