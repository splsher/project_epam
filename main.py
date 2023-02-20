import json
from flask import Flask, g, jsonify, request, render_template, make_response
from flask_cors import CORS, cross_origin
from flask import Flask, g, request, jsonify
from flask_bcrypt import Bcrypt
from requests import Session
from requests.auth import HTTPBasicAuth
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager, get_jwt
from models import User, Session


app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
jwt = JWTManager(app)


bcrypt = Bcrypt(app)
# auth = HTTPBasicAuth()
session = Session()
app.config["DEBUG"] = True
DATABASE = "./test.db"


def get_db():
    db = getattr(g, '_database', None)


@app.route('/', methods=['GET'])
def home():
    return "Backend"


@app.route('/signup', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=bcrypt.generate_password_hash(
            data['password']).decode('utf-8'),
        city=data['city'],
        photo=data['photo']
    )

    if not session.query(User).filter(User.username == data['username']).one_or_none() is None:
        return 'This username already exists', '400'

    if not session.query(User).filter(User.email == data['email']).one_or_none() is None:
        return 'This email is taken', '400'

    session.add(new_user)
    session.commit()

    return jsonify({'message': 'successful operation'})


@app.route('/login', methods=['POST'])
# @auth.verify_password
def login():
    auth = json.loads(request.data)
    # print('az', auth)
    # if not auth or not auth.username or not auth.password:
    #     return make_response('could not verify', 401, {'WWW.Authantication': 'Basic realm:"login require"'})

    user = session.query(User).filter(
        User.username == auth['username']).one_or_none()
    if user is None:
        return 'User with such username was not found'

    # if not bcrypt.check_password_hash(user.password, auth.password):
    #     return 'Wrong password'

    access_token = create_access_token(identity=user.id)

    return jsonify({'token': access_token})


@app.route('/edit_profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    current_user = get_jwt_identity()
    if current_user is None:
        return make_response(jsonify({"403": "Access is denied"}), 403)

    find_user = session.query(User).filter(User.id == current_user).one_or_none()
    if find_user is None:
        return 'User not found'

    data = request.get_json()

    if not session.query(User).filter(User.username == data['username']).one_or_none() is None:
        return 'This username already exists', '400'

    if not session.query(User).filter(User.email == data['email']).one_or_none() is None:
        return 'This email is taken', '400'

    find_user.username = data['username']
    find_user.email = data['email']
    find_user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    find_user.city = data['city']
    find_user.photo = data['photo']

    session.commit()

    return jsonify({'message': 'successful operation'})


if __name__ == "__main__":
    # socketio.run(app)
    app.run()
