from flask import Blueprint, request
from application import User, Role, db
from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

app = Blueprint("user", __name__, url_prefix="/users")


# 1. Padronizar a saída
def user_response(user):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": {
            "id": user.role_id,
            "name": user.role.name
        }
    }


# 2. get_current_user para vertificar a role do usuário
def get_current_user():
    user_id = int(get_jwt_identity())
    return db.get_or_404(User, user_id)


# 4. verificar role admin
def is_admin(user):
    return user.role and user.role.name == "admin"


# 5. verificar role regular
def is_regular(user):
    return user.role and user.role.name == "regular"


# 7. create_user passa a ter autorização baseado nas roles
@app.post("/")
@jwt_required()
def create_user():
    current_user = get_current_user()

    if not is_admin(current_user):
        return {
            "msg": "Apenas administradores podem criar usuários."
        }, HTTPStatus.FORBIDDEN

    data = request.get_json()

    if not data:
        return {
            "error": "Dados ausentes"
        }, HTTPStatus.BAD_REQUEST

    if "username" not in data or "password" not in data:
        return {
            "error": "Os campos 'username' e 'password' são obrigatórios"
        }, HTTPStatus.BAD_REQUEST

    username = data["username"]
    email = data.get("email")
    password = data["password"]
    role_id = data.get("role_id")

    if User.query.filter_by(username=username).first():
        return {
            "error": "O username já existe"
        }, HTTPStatus.CONFLICT

    if not role_id:
        return {
            "error": "O campo 'role_id' é obrigatório"
        }, HTTPStatus.BAD_REQUEST

    role = db.session.get(Role, role_id)
    if not role:
        return {
            "error": "O 'role_id' informado não existe"
        }, HTTPStatus.BAD_REQUEST

    user = User(username=username, email=email, role_id=role_id)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user_response(user), HTTPStatus.CREATED


# 6. list_users passa a ter autorização baseado nas roles
@app.get("/")
@jwt_required()
def list_users():
    current_user = get_current_user()

    if not (is_admin(current_user) or is_regular(current_user)):
        return {"msg": "Apenas administradores e usuários regulares podem acessar esse recurso."}, HTTPStatus.FORBIDDEN

    query = db.select(User)
    result = db.session.execute(query)
    users = result.scalars().all()

    return [user_response(user) for user in users], HTTPStatus.OK


# 3. get_user passa a ter autorização baseado nas roles
@app.get("/<int:user_id>")
@jwt_required()
def get_user(user_id):
    current_user = get_current_user()

    if not (is_admin(current_user) or is_regular(current_user)):
        return {"msg": "Apenas administradores e usuários regulares podem acessar esse recurso."}, HTTPStatus.FORBIDDEN

    user = db.get_or_404(User, user_id)
    return user_response(user), HTTPStatus.OK


# 10. update_user_partial passa a ter autorização baseado nas roles
@app.patch("/<int:user_id>")
@jwt_required()
def update_user_partial(user_id):
    current_user = get_current_user()

    if not is_admin(current_user):
        return {"msg": "Apenas administradores podem atualizar usuários."}, HTTPStatus.FORBIDDEN

    user = db.get_or_404(User, user_id)

    data = request.get_json()
    if not data:
        return {"error": "Dados ausentes"}, HTTPStatus.BAD_REQUEST

    # 11. considerando os novos campos
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.set_password(data["password"])
    if "role_id" in data:
        role = db.session.get(Role, data["role_id"])
        if not role:
            return {"error": "O 'role_id' informado não existe"}, HTTPStatus.BAD_REQUEST
        user.role_id = role.id

    db.session.commit()

    return user_response(user), HTTPStatus.OK


# 8. update_user_full passa a ter autorização baseado nas roles
@app.put("/<int:user_id>")
@jwt_required()
def update_user_full(user_id):
    current_user = get_current_user()

    if not is_admin(current_user):
        return {"msg": "Apenas administradores podem atualizar usuários."}, HTTPStatus.FORBIDDEN

    user = db.get_or_404(User, user_id)

    data = request.get_json()
    if not data or "username" not in data or "email" not in data or "password" not in data or "role_id" not in data:
        return {
            "error": "Os campos 'username', 'email', 'password' e 'role_id' são obrigatórios"
        }, HTTPStatus.BAD_REQUEST

    # 9. considerando todos oscampos
    user.username = data["username"]
    user.email = data["email"]
    user.set_password(data["password"])

    role = db.session.get(Role, data["role_id"])
    if not role:
        return {"error": "O 'role_id' informado não existe"}, HTTPStatus.BAD_REQUEST
    user.role_id = role.id

    db.session.commit()

    return user_response(user), HTTPStatus.OK


# 12. delete_user passa a ter autorização baseado nas roles
@app.delete("/<int:user_id>")
@jwt_required()
def delete_user(user_id):
    current_user = get_current_user()

    if not is_admin(current_user):
        return {
            "msg": "Apenas administradores podem remover usuários."
        }, HTTPStatus.FORBIDDEN

    user = db.get_or_404(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return "", HTTPStatus.NO_CONTENT
