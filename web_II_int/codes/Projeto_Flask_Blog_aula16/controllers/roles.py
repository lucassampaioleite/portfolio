from flask import Blueprint, request
from models import Role, User
from extensions import db
from http import HTTPStatus
from views import RoleView

from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint("roles", __name__, url_prefix="/roles")


def get_current_user():
    user_id = int(get_jwt_identity())
    return db.get_or_404(User, user_id)


def is_admin(user):
    return user.role and user.role.name == "admin"


def is_regular(user):
    return user.role and user.role.name == "regular"


@app.post("/")
@jwt_required()
def create_role():
    current_user = get_current_user()

    if not is_admin(current_user):
        return {"msg": "Apenas administradores podem criar roles."}, HTTPStatus.FORBIDDEN

    data = request.get_json()
    if not data or "name" not in data:
        return {"error": "O campo 'name' é obrigatório"}, HTTPStatus.BAD_REQUEST

    if Role.query.filter_by(name=data["name"]).first():
        return {"error": "Essa role já existe"}, HTTPStatus.CONFLICT

    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()

    return RoleView.response(role), HTTPStatus.CREATED


@app.get("/")
@jwt_required()
def list_roles():
    current_user = get_current_user()

    if not (is_admin(current_user) or is_regular(current_user)):
        return {"msg": "Apenas administradores e usuários regulares podem acessar esse recurso."}, HTTPStatus.FORBIDDEN

    roles = Role.query.all()
    return RoleView.list_response(roles), HTTPStatus.OK


@app.get("/<int:role_id>")
@jwt_required()
def get_role(role_id):
    current_user = get_current_user()

    if not (is_admin(current_user) or is_regular(current_user)):
        return {"msg": "Apenas administradores e usuários regulares podem acessar esse recurso."}, HTTPStatus.FORBIDDEN

    role = db.get_or_404(Role, role_id)
    return RoleView.response(role), HTTPStatus.OK


@app.put("/<int:role_id>")
@jwt_required()
def update_role(role_id):
    current_user = get_current_user()

    if not is_admin(current_user):
        return {"msg": "Apenas administradores podem atualizar roles."}, HTTPStatus.FORBIDDEN

    role = db.get_or_404(Role, role_id)
    data = request.get_json()

    if not data or "name" not in data:
        return {"error": "O campo 'name' é obrigatório"}, HTTPStatus.BAD_REQUEST

    role.name = data["name"]
    db.session.commit()

    return RoleView.response(role), HTTPStatus.OK


@app.delete("/<int:role_id>")
@jwt_required()
def delete_role(role_id):
    current_user = get_current_user()

    if not is_admin(current_user):
        return {"msg": "Apenas administradores podem deletar roles."}, HTTPStatus.FORBIDDEN

    role = db.get_or_404(Role, role_id)

    if role.users:
        return {
            "error": "Não é possível deletar uma role que está atribuída a usuários."
        }, HTTPStatus.CONFLICT

    db.session.delete(role)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
