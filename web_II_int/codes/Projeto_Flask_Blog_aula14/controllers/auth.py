from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from application import User


app = Blueprint("auth", __name__, url_prefix="/auth")


@app.post("/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not data or not username or not password:
        return {"msg": "Username and password required"}, HTTPStatus.BAD_REQUEST

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

    access_token = create_access_token(identity=user.username)
    return {"access_token": access_token}, HTTPStatus.OK




# @app.post("/login")
# def login():
#     username = request.json.get("username")
#     password = request.json.get("password")

#     if not username or not password:
#         return {"msg": "Username and password required"}, HTTPStatus.BAD_REQUEST

#     user = User.query.filter_by(username=username).first()

#     if user is None or not user.check_password(password):
#         return {"msg": "Bad username or password"}, HTTPStatus.UNAUTHORIZED

#     access_token = create_access_token(
#         identity=user.id)  # pode usar id ou username
#     return {"access_token": access_token}
