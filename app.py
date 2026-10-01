import os
from flask import Flask, render_template
from flask_login import LoginManager
from config import Config
from models import db, User
from routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize Extensions
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register Blueprints
    app.register_blueprint(main_blueprint)

    # Global Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('base.html', page_error="404 Page Not Found"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('base.html', page_error="500 Internal Server Error"), 500

    # Auto-create database tables if not exist
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    print("Starting Smart Recruitment System on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
