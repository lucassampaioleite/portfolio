import os
import click
from flask import Flask, current_app
from extensions import db
from extensions import jwt

from models import User, Role


@click.command("init-db")
def init_db_command():
    with current_app.app_context():
        db.create_all()

        # cria a role "admin" se não existir
        role_admin = Role.query.filter_by(name="admin").first()
        if not role_admin:
            role_admin = Role(name="admin")
            db.session.add(role_admin)
            db.session.commit()
            click.echo("Role 'admin' criada!")

        # cria um usuário "admin" se não existir
        if not User.query.filter_by(username="admin").first():
            user = User(username="admin",
                        email="admin@example.com", role=role_admin)
            user.set_password("admin123")
            db.session.add(user)
            db.session.commit()
            click.echo("Usuário admin criado!")
        else:
            click.echo("Usuário admin já existe.")

    click.echo("Inicializando a base de dados...")


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='sqlite:///blog.sqlite',
        JWT_SECRET_KEY="super-secret"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.cli.add_command(init_db_command)

    db.init_app(app)
    jwt.init_app(app)

    from controllers import user, auth, roles
    app.register_blueprint(user.app)
    app.register_blueprint(auth.app)
    app.register_blueprint(roles.app)

    return app
