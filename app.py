import os
from flask import Flask
from config import Config
from models import db, login_manager
from flask_migrate import Migrate
from routes.public import public_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.members import members_bp
from routes.plans import plans_bp
from routes.payments import payments_bp
from routes.attendance import attendance_bp
from routes.trainers import trainers_bp
from models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(members_bp, url_prefix='/admin/members')
    app.register_blueprint(plans_bp, url_prefix='/admin/plans')
    app.register_blueprint(payments_bp, url_prefix='/admin/payments')
    app.register_blueprint(attendance_bp, url_prefix='/admin/attendance')
    app.register_blueprint(trainers_bp, url_prefix='/admin/trainers')

    # Context processors for template globals
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.now()}

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
