from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:consultadd@localhost:3306/mydatabase'
    app.config['SECRET_KEY'] = 'secret_key'

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Import models inside the app context
    from app.models import User  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Fix: Ensures user is loaded from DB

    # Import blueprints
    from app.routes.auth import auth
    from app.routes.members import members

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(members)

    with app.app_context():
        db.create_all()

    return app
