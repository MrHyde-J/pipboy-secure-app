from flask import render_template, request, redirect, url_for, flash, jsonify, abort, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import bleach

# FIX: Import db from your extensions or models to avoid circular import with 'app'
from models import User, db 
from security import InputValidator, SecurityMonitor

def init_routes(app):
    """Initialize all routes"""
    
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = InputValidator.sanitize_input(request.form.get('username', ''))
            password = request.form.get('password', '')
            
            if SecurityMonitor.check_rate_limit(username):
                flash('Too many failed attempts. Please try again in 5 minutes.', 'error')
                return render_template('login.html')
            
            user = User.query.filter_by(username=username).first()
            
            # Use the check_password method from your User model
            is_valid = user and user.check_password(password)
            
            SecurityMonitor.record_login_attempt(
                username, 
                success=is_valid,
                user_agent=request.user_agent.string[:200]
            )
            
            if is_valid:
                # FIX: Check the correct active attribute from your User model
                # We renamed this to is_active_user in the model fix to avoid conflict
                if hasattr(user, 'is_active_user') and not user.is_active_user:
                    flash('Account is deactivated', 'error')
                    return render_template('login.html')
                
                login_user(user)
                user.update_last_login()
                
                flash(f'Welcome back, {username}!', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page if next_page and not next_page.startswith('//') else url_for('dashboard'))
            else:
                flash('Invalid credentials.', 'error')
                return render_template('login.html')
        
        return render_template('login.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        
        if request.method == 'POST':
            username = InputValidator.sanitize_input(request.form.get('username', ''))
            email = InputValidator.sanitize_input(request.form.get('email', ''))
            password = request.form.get('password', '')
            
            # Check if exists
            if User.query.filter((User.username == username) | (User.email == email)).first():
                flash('Username or Email already exists', 'error')
                return render_template('register.html')
            
            try:
                new_user = User(username=username, email=email, role='user')
                new_user.set_password(password)
                
                db.session.add(new_user)
                db.session.commit()
                
                flash('Registration successful!', 'success')
                return redirect(url_for('login'))
            except Exception:
                db.session.rollback()
                flash('Registration failed.', 'error')
                return render_template('register.html')
        
        return render_template('register.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        return render_template('dashboard.html')
    
    @app.route('/admin')
    @login_required
    def admin_panel():
        # FIX: Ensure is_admin property is used correctly (no parentheses if it's a property)
        if not current_user.is_admin:
            abort(403)
        
        users = User.query.order_by(User.created_at.desc()).all()
        return render_template('admin_panel.html', users=users)
    
    @app.route('/strength-tester')
    @login_required
    def strength_tester():
        return render_template('strength_tester.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('login'))

    # Error Handlers (Moved inside init_routes to use the 'app' instance)
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403