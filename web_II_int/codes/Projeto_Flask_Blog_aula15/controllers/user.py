from flask import Blueprint, request
from application import User, db
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint("user", __name__, url_prefix="/users")


@app.post("/")
@jwt_required()
def create_user():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return {"error": "username e password é obrigatório"}, HTTPStatus.BAD_REQUEST

    username = data["username"]
    email = data.get("email")
    password = data["password"]
    role_id = data["role_id"]

    if User.query.filter_by(username=username).first():
        return {"error": "username já existe"}, HTTPStatus.CONFLICT

    user = User(username=username, email=email, role_id=role_id)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }, HTTPStatus.CREATED


# @app.post("/")
# @jwt_required()
# def create_user():
#     data = request.get_json()

#     if not data or "username" not in data:
#         return {"error": "username é obrigatório"}, HTTPStatus.BAD_REQUEST

#     email = data.get("email")

#     user = User(username=data["username"], email=email)

#     db.session.add(user)
#     db.session.commit()

#     return {
#         "id": user.id,
#         "username": user.username,
#         "email": user.email
#     }, HTTPStatus.CREATED


@app.get("/")
@jwt_required()
def list_users():

    user_id = int(get_jwt_identity())
    user = db.get_or_404(User, user_id)
    
    if user.role.name != "admin":
        return {"msg": "Usuário não possui acesso."}, HTTPStatus.FORBIDDEN

    query = db.select(User)
    result = db.session.execute(query)
    users = result.scalars().all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": {
                "id": user.role_id,
                "name": user.role.name
            }
        }
        for user in users
    ], HTTPStatus.OK


@app.get("/<int:user_id>")
def get_user(user_id):
    user = db.get_or_404(User, user_id)

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }, HTTPStatus.OK


@app.patch("/<int:user_id>")
def update_user_partial(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()

    if not data:
        return {"error": "Dados ausentes"}, HTTPStatus.BAD_REQUEST

    username = data.get("username")
    email = data.get("email")

    if username:
        user.username = username
    if email:
        user.email = email

    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }, HTTPStatus.OK


@app.put("/<int:user_id>")
def update_user_full(user_id):
    user = db.get_or_404(User, user_id)
    data = request.get_json()

    if not data or "username" not in data or "email" not in data:
        return {"error": "Os campos username e email são obrigatórios"}, HTTPStatus.BAD_REQUEST

    user.username = data["username"]
    user.email = data["email"]

    db.session.commit()

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }, HTTPStatus.OK


@app.delete("/<int:user_id>")
def delete_user(user_id):
    user = db.get_or_404(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
