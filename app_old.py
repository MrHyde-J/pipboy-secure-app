from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'vault-tec-secure-key-2077'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipboy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = 1800

# Initialize extensions FIRST
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '// ACCESS DENIED: Authentication required //'
login_manager.login_message_category = 'error'

# Now import models AFTER db is created
from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Import routes
from routes import init_routes
init_routes(app)

if __name__ == '__main__':
    # Initialize database within app context
    with app.app_context():
        db.create_all()
        
        # Create default users if they don't exist
        if not User.query.filter_by(username='vault_admin').first():
            from werkzeug.security import generate_password_hash
            admin = User(
                username='vault_admin',
                email='admin@vault-tec.com',
                role='admin',
                password_hash=generate_password_hash('Vault-Tec2077!')
            )
            db.session.add(admin)
        
        if not User.query.filter_by(username='wastelander').first():
            from werkzeug.security import generate_password_hash
            user = User(
                username='wastelander',
                email='wastelander@ncr.com',
                role='user',
                password_hash=generate_password_hash('NCR!2024')
            )
            db.session.add(user)
        
        db.session.commit()
        print("✓ Database initialized!")
        print("Admin: vault_admin / Vault-Tec2077!")
        print("User: wastelander / NCR!2024")
    
    print("\nStarting Flask server...")
    print("Access: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)