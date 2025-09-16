from flask import Blueprint, request
from application import Role, db
from http import HTTPStatus

from flask_jwt_extended import jwt_required

app = Blueprint("roles", __name__, url_prefix="/roles")


@app.post("/")
@jwt_required()
def create_role():
    data = request.get_json()
    role = Role(name=data["name"])
    db.session.add(role)
    db.session.commit()
    
    return {
        "msg": "Role criada!"
    }, HTTPStatus.CREATED

