#!/usr/bin/env python3
"""
Initialize the database for Vault-Tec Secure System
"""

import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def init_database():
    """Initialize database with default data"""
    print("Initializing Vault-Tec database...")
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Created database tables")
        
        # Create admin user
        admin = User.query.filter_by(username='vault_admin').first()
        if not admin:
            admin = User(
                username='vault_admin',
                email='admin@vault-tec.com',
                role='admin'
            )
            admin.set_password('Vault-Tec2077!')
            db.session.add(admin)
            print("✓ Created admin user: vault_admin / Vault-Tec2077!")
        
        # Create regular user
        user = User.query.filter_by(username='wastelander').first()
        if not user:
            user = User(
                username='wastelander',
                email='wastelander@ncr.com',
                role='user'
            )
            user.set_password('NCR!2024')
            db.session.add(user)
            print("✓ Created user: wastelander / NCR!2024")
        
        try:
            db.session.commit()
            print("✓ Database initialized successfully!")
            print("\nDefault accounts created:")
            print("  Admin: vault_admin / Vault-Tec2077!")
            print("  User: wastelander / NCR!2024")
            print("\nRun the application with: python app.py")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"✗ Error initializing database: {e}")
            return False

if __name__ == '__main__':
    init_database()