from flask import Blueprint, request
from http import HTTPStatus
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from application import jwt
from models import User

app = Blueprint("auth", __name__, url_prefix="/auth")

jwt_blacklist = set()


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

    access_token = create_access_token(identity=str(user.id))
    return {"access_token": access_token}, HTTPStatus.OK


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  
    return jti in jwt_blacklist


@app.post("/logout")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    jwt_blacklist.add(jti)  
    return {"msg": "Logout realizado com sucesso"}, HTTPStatus.OK
