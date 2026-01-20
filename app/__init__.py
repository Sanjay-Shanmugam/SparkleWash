from flask import Flask
from flask_login import LoginManager
from .database import get_db_connection

def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey'  # Change for production

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        conn = get_db_connection()
        user_data = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()
        if user_data:
            return User(user_data['id'], user_data['name'], user_data['email'], user_data['role'], 
                       user_data['phone'], user_data['vehicle_no'], user_data['vehicle_type'])
        return None

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
