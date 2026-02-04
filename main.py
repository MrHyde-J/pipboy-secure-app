from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import re
import random

# ============================================
# INITIALIZATION
# ============================================
app = Flask(__name__, 
    static_folder='static',
    static_url_path='/static'
)

app.config['SECRET_KEY'] = 'vault-tec-secure-key-2077'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pipboy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = '// ACCESS DENIED: Authentication required //'
login_manager.login_message_category = 'error'

# ============================================
# MODELS
# ============================================
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def update_last_login(self):
        self.last_login = datetime.utcnow()
        db.session.commit()
        
    def get_status_color(self):
        """Return status color based on activity"""
        if not self.last_login:
            return "#FF9900"  # Orange - never logged in
        days_since = (datetime.utcnow() - self.last_login).days
        if days_since < 1:
            return "#00FF00"  # Green - active today
        elif days_since < 7:
            return "#FFFF00"  # Yellow - active this week
        else:
            return "#FF3300"  # Red - inactive

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============================================
# PASSWORD STRENGTH METER
# ============================================
class PasswordStrengthMeter:
    def __init__(self):
        self.common_passwords = [
            'password', '123456', '12345678', '123456789', '12345',
            'qwerty', 'abc123', 'password1', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'football', 'baseball'
        ]
    
    def calculate_strength(self, password):
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 15
            if len(password) >= 12:
                score += 10
            else:
                feedback.append("Consider longer sequence (12+ characters)")
        else:
            feedback.append("Minimum 8 characters required")
        
        # Character variety
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        
        if has_upper:
            score += 15
        else:
            feedback.append("Add UPPERCASE letters")
        
        if has_lower:
            score += 15
        else:
            feedback.append("Add lowercase letters")
        
        if has_digit:
            score += 15
        else:
            feedback.append("Add numbers (0-9)")
        
        if has_special:
            score += 20
        else:
            feedback.append("Add special characters")
        
        # Common password check
        if password.lower() in self.common_passwords:
            score = max(10, score - 30)
            feedback.insert(0, "CRITICAL: Common password detected")
        
        # Final score
        score = min(100, max(0, score))
        
        # Categorization
        if score >= 80:
            category = "STRONG // VAULT-TEC APPROVED"
            color = "#00FF00"
        elif score >= 60:
            category = "GOOD // SECURE"
            color = "#99FF33"
        elif score >= 40:
            category = "MODERATE // ACCEPTABLE"
            color = "#FFFF00"
        elif score >= 20:
            category = "WEAK // SECURITY RISK"
            color = "#FF9900"
        else:
            category = "CRITICAL FAILURE"
            color = "#FF3300"
        
        return {
            'score': score,
            'category': category,
            'color': color,
            'feedback': feedback,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'scan_id': f"SCAN-{datetime.now().timestamp():.0f}"
        }

# ============================================
# CONTEXT PROCESSORS
# ============================================
@app.context_processor
def inject_session_data():
    """Inject session data into all templates"""
    return {
        'session': session,
        'current_year': datetime.now().year,
        'random_rads': f"{random.uniform(0.0, 0.5):.1f}",
        'system_time': datetime.now().strftime("%H:%M:%S")
    }

# ============================================
# ROUTES
# ============================================
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
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            user.update_last_login()
            
            # Generate session ID for display
            session['login_time'] = datetime.now().strftime("%H:%M:%S")
            session['session_id'] = f"VT-{random.randint(10000, 99999)}"
            
            flash(f'ACCESS GRANTED. Welcome, {username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('ERROR: Invalid credentials. Access denied.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username', '')
        email = request.form.get('email', '')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        errors = []
        
        if not username or len(username) < 3:
            errors.append('Username must be at least 3 characters')
        
        if not email or '@' not in email:
            errors.append('Valid email required')
        
        if not password or len(password) < 8:
            errors.append('Password must be at least 8 characters')
        
        if password != confirm_password:
            errors.append('Passwords do not match')
        
        if User.query.filter_by(username=username).first():
            errors.append('Username already exists')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered')
        
        if errors:
            for error in errors:
                flash(f'ERROR: {error}', 'error')
        else:
            new_user = User(username=username, email=email, role='user')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('SUCCESS: Registration complete! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Generate some stats for the dashboard
    user_count = User.query.count()
    admin_count = User.query.filter_by(role='admin').count()
    
    # Get recent users (last 5)
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', 
                         user_count=user_count,
                         admin_count=admin_count,
                         recent_users=recent_users)

@app.route('/strength-tester')
@login_required
def strength_tester():
    return render_template('strength_tester.html')

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin():
        flash('ERROR: Insufficient clearance level.', 'error')
        return redirect(url_for('dashboard'))
    
    users = User.query.all()
    return render_template('admin_panel.html', users=users)

@app.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    session.clear()
    flash(f'SESSION TERMINATED. Goodbye, {username}!', 'info')
    return redirect(url_for('login'))

@app.route('/api/check-password', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')
    
    if not password:
        return jsonify({'error': 'No password provided'}), 400
    
    meter = PasswordStrengthMeter()
    result = meter.calculate_strength(password)
    return jsonify(result)

@app.route('/pipboy-radio')
@login_required
def pipboy_radio():
    """Pip-Boy radio station (Easter egg)"""
    stations = [
        {"name": "Galaxy News Radio", "freq": "97.2 FM", "desc": "Three Dog, AWOOOO!"},
        {"name": "Enclave Radio", "freq": "102.5 FM", "desc": "Truth is on the airwaves."},
        {"name": "Vault-Tec Emergency", "freq": "108.5 FM", "desc": "Security broadcasts only."},
        {"name": "Mojave Music Radio", "freq": "95.3 FM", "desc": "Big Iron on his hip..."},
    ]
    return render_template('radio.html', stations=stations)

@app.route('/system-status')
@login_required
def system_status():
    """System status page"""
    status_info = {
        'database': {
            'status': 'OPERATIONAL',
            'color': '#00FF00',
            'details': f'{User.query.count()} users registered'
        },
        'security': {
            'status': 'ACTIVE',
            'color': '#00FF00',
            'details': 'All protocols engaged'
        },
        'network': {
            'status': 'STABLE',
            'color': '#99FF33',
            'details': f'Session: {session.get("session_id", "N/A")}'
        },
        'encryption': {
            'status': 'ENABLED',
            'color': '#00FF00',
            'details': 'PBKDF2-SHA256 260k iterations'
        }
    }
    return render_template('system_status.html', status_info=status_info)

@app.route('/api/geiger-click', methods=['POST'])
def geiger_click():
    """API endpoint for geiger counter clicks"""
    intensity = random.uniform(0.1, 1.0)
    return jsonify({
        'intensity': intensity,
        'timestamp': datetime.now().isoformat(),
        'radiation': f"{random.uniform(0.0, 0.5):.2f} RADS"
    })

@app.route('/force-css')
def force_css():
    return '''
    <style>
        /* Force all styles inline */
        body { 
            background: #000000 !important; 
            color: #00CC00 !important; 
            font-family: 'Courier New', monospace !important;
        }
        .pipboy-screen { 
            background: #001100 !important; 
            border: 3px solid #00FF00 !important; 
            padding: 20px; 
            margin: 20px auto; 
            max-width: 900px;
        }
        h1, h2, h3 { color: #00FF00 !important; }
        .pipboy-input { 
            background: rgba(0,20,0,0.8) !important; 
            border: 2px solid #00FF00 !important; 
            color: #00FF00 !important; 
            padding: 10px; 
            width: 100%;
        }
        .pipboy-btn { 
            background: rgba(0,40,0,0.8) !important; 
            border: 2px solid #00FF00 !important; 
            color: #00CC00 !important; 
            padding: 10px 20px;
        }
    </style>
    <script>
        // Apply styles to existing page
        document.addEventListener('DOMContentLoaded', function() {
            document.body.style.cssText = 'background: #000000 !important; color: #00CC00 !important; font-family: "Courier New", monospace !important;';
            
            var screens = document.querySelectorAll('.pipboy-screen');
            screens.forEach(function(screen) {
                screen.style.cssText = 'background: #001100 !important; border: 3px solid #00FF00 !important; padding: 20px; margin: 20px auto; max-width: 900px;';
            });
        });
    </script>
    '''

# ============================================
# ERROR HANDLERS
# ============================================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

# ============================================
# MAIN EXECUTION
# ============================================
if __name__ == '__main__':
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create default admin if not exists
        if not User.query.filter_by(username='vault_admin').first():
            admin = User(
                username='vault_admin',
                email='admin@vault-tec.com',
                role='admin'
            )
            admin.set_password('Vault-Tec2077!')
            db.session.add(admin)
            print("✓ Created admin: vault_admin / Vault-Tec2077!")
        
        # Create default user if not exists
        if not User.query.filter_by(username='wastelander').first():
            user = User(
                username='wastelander',
                email='wastelander@ncr.com',
                role='user'
            )
            user.set_password('NCR!2024')
            db.session.add(user)
            print("✓ Created user: wastelander / NCR!2024")
        
        db.session.commit()
    
    print("\n" + "="*60)
    print("        VAULT-TEC PIP-BOY 3000 SECURE SYSTEM")
    print("="*60)
    print("Database initialized successfully!")
    print("\nAccess the application at: http://localhost:5000")
    print("\nDefault accounts:")
    print("  Admin: vault_admin / Vault-Tec2077!")
    print("  User: wastelander / NCR!2024")
    print("\nFeatures:")
    print("  ✓ Authentic Pip-Boy 3000 interface")
    print("  ✓ Password strength analyzer")
    print("  ✓ Role-based access control")
    print("  ✓ CRT scanline effects")
    print("  ✓ Geiger counter animation")
    print("  ✓ Boot sequence")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)