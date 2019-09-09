from config import config
from database import db
from flask import Flask, url_for
from flask_babel import Babel
from flask_materialize import Material
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, MigrateCommand

babel = Babel()
material = Material()
migrate = Migrate()
nav = Nav()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

@nav.navigation()
def navbar():
    if current_user.is_authenticated:
        return Navbar('fl[]w',
            View('Home', 'main.index'),
            View('Projects', 'admin.projects'),
            View('Logout', 'auth.logout'))
    else:
        return Navbar('fl[]w')

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    material.init_app(app)
    babel.init_app(app)
    nav.init_app(app)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.api.v1 import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
