import json
from datetime import datetime
import requests
from flask import Flask, g, jsonify, request, render_template, make_response
from flask_cors import CORS, cross_origin
from flask import Flask, g, request, jsonify
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, JWTManager
from models.models import User, Session, Wall
from schemes import WallSchema

app = Flask(__name__, template_folder='templates', static_folder='static')

# app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()
session = Session()
app.config["DEBUG"] = True
DATABASE = "./test.db"


@app.route('/', methods=["POST", "GET"])
def login_web():
    if request.method == "POST":
        if request.form["username"] != "" and request.form["password"] != "":
            username = request.form["username"]
            password = request.form["password"]
    return render_template('login.html')


# @app.route('/signup', methods=["POST", "GET"])
# def register():
#     return render_template('registration.html')


# @app.route('/wall')
# def display_new():
#     return render_template('wall.html', title='The news')
#
#
# @app.route('/login_2')
# def login_2():
#     return render_template('index.html', title="Login 2")


def get_db():
    db = getattr(g, '_database', None)


# @app.route('/', methods=['GET'])
# def home():
#     return "Welcome to my project🪐"


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

# @app.route('/login', methods=['POST'])
# @auth.verify_password
# def login():
#     auth = json.loads(request.data)
#     print('az', auth)
#
#     user = session.query(User).filter(
#         User.username == auth['username']).one_or_none()
#     if user is None:
#         return 'User with such username was not found'
#
#     # if not bcrypt.check_password_hash(user.password, auth.password):
#     #     return 'Wrong password'
#
#     access_token = create_access_token(identity=user.id)
#
#     return jsonify({'token': access_token})

@app.route('/login', methods=['POST'])
@auth.verify_password
def login():
    auth = json.loads(request.data)
    print('az', auth)

    user = session.query(User).filter(User.username == auth['username']).all()
    if not user:
        return 'User with such username was not found'
    elif len(user) > 1:
        return 'Multiple users found with the same username'

    user = user[0]

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


@app.route('/wall', methods=['POST'])
@jwt_required()
def create_news():
    current_user = get_jwt_identity()
    if current_user is None:
        return make_response(jsonify({"403": "Access is denied"}), 403)

    data = request.get_json()
    new = Wall(
        user_id=current_user,
        datetime=datetime.utcnow(),
        title=data['title'],
        text=data['text'],
        photo_wall=data['photo']
    )

    session.add(new)
    session.commit()

    return jsonify({'message': 'successful operation!'})


@app.route('/news', methods=['GET'])
@jwt_required()
def display_news():
    current_user = get_jwt_identity()
    if current_user is None:
        return make_response(jsonify({"403": "Access is denied"}), 403)

    found_news = session.query(Wall).all()
    news = []

    for new in found_news:
        news.append(WallSchema().dump(new))
    return jsonify(news)


@app.route("/delete_news", methods=['DELETE'])
@jwt_required()
def delete_news():
    global new
    current_user = get_jwt_identity()
    if current_user is None:
        return make_response(jsonify({"403": "Access is denied"}), 403)
    found_news = session.query(Wall).all()
    news = []

    for new in found_news:
        news.append(WallSchema().dump(new))

    session.delete(new)
    session.commit()

    return jsonify({'message': 'successful operation'})


if __name__ == '__main__':
    # socketio.run(app)
    app.run()
