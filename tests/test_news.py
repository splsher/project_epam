from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from models.models import User
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__, template_folder='templates', static_folder='static')

jwt = JWTManager(app)


@pytest.fixture
def jwt_token():
    engine = create_engine('mysql+pymysql://root:Bonia9977@localhost/social_network')
    Session = sessionmaker(bind=engine)
    session = Session()

    user = User(username='tester', email='tester@example.com', password='test123', city='test city', photo='test.png')
    session.add(user)
    session.commit()

    access_token = create_access_token(identity=user.id)
    yield access_token

    session.delete(user)
    session.commit()


#

def test_display_news(client, jwt_token):
    response = client.get('/news', headers={'Authorization': 'Bearer ' + jwt_token})
    assert response.status_code == 200
    assert len(response.json) == 0
