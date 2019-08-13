from flask import Flask
from app1.extension import jwt, client
from app1.config import App_Config
from app1 import api as api


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    acc = client.db.user.find_one({"_id": identity})
    if acc['role'] == "admin":
        return {"is_admin": True}
    return {"is_admin": False}


def register_blueprint(app):
    app.register_blueprint(api.account.api, url_prefix='/api/account')
    app.register_blueprint(api.leave_of_absence_form.api, url_prefix='/api/leave_form')


def register_extensions(app, content, config_object):

    client.app = app
    client.init_app(app)
    # don't start extensions if content != app
    if content == 'app':
        jwt.init_app(app)


def create_app(config_object=App_Config, content='app'):

    app = Flask(__name__, static_url_path="", static_folder="./template", template_folder="./template")
    app.config.from_object(config_object)
    register_extensions(app, content, config_object)
    register_blueprint(app)
    return app


app = create_app()
app.run()
