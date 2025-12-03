import bcrypt
from flask import request, jsonify, Blueprint
from api.models import db, User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)


@api.route('/hello', methods=['GET'])
def hello1():
    return ({"msg": "hello"}, 200)


@api.route('/signup', methods=['POST'])
def signup():

    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    exists = User.query.filter_by(email=email).first()
    if exists:
        return jsonify({"msg": "User already exists"}), 400

    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(email=email, password=hashed.decode(
        "utf-8"), is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created"}), 201


@api.route('/token', methods=['POST'])
def login():

    email = request.json.get("email")
    password = request.json.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing credentials"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
        return jsonify({"msg": "Invalid credentials"}), 401

    token = create_access_token(identity=user.id)

    return jsonify({
        "token": token,
        "user_id": user.id
    }), 200
