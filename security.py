import bleach
import re
from html import escape
from datetime import datetime, timedelta
from flask import request, current_app
from models import LoginAttempt, SecurityLog, db

class InputValidator:
    """Prevent SQL Injection & XSS attacks"""
    
    @staticmethod
    def sanitize_input(input_string, max_length=100, allow_html=False):
        """Sanitize user input to prevent XSS attacks"""
        if not input_string:
            return ''
        
        # Convert to string and truncate
        sanitized = str(input_string)[:max_length]
        
        # Remove harmful characters
        if not allow_html:
            # Strip all HTML tags
            sanitized = bleach.clean(
                sanitized,
                tags=[],  # No HTML tags allowed
                attributes={},
                styles=[],
                strip=True
            )
        
        # Escape HTML entities
        sanitized = escape(sanitized)
        
        return sanitized
    
    @staticmethod
    def validate_username(username):
        """Validate username format"""
        if not username or len(username) < 3 or len(username) > 50:
            return False
        
        # Allow letters, numbers, underscores, hyphens
        pattern = r'^[a-zA-Z0-9_-]+$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password):
        """Validate password meets minimum requirements"""
        if not password or len(password) < 8:
            return False
        
        # Check for at least one of each: uppercase, lowercase, number
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        
        return bool(has_upper and has_lower and has_digit)
    
    @staticmethod
    def sanitize_sql_query(query_params):
        """Prevent SQL injection - Use parameterized queries instead"""
        # This method demonstrates the concept
        # In practice, use SQLAlchemy's parameterized queries
        dangerous_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT', 'UNION', 'OR', 'AND', '--', ';']
        
        for param in query_params.values():
            param_str = str(param).upper()
            for keyword in dangerous_keywords:
                if keyword in param_str and f' {keyword} ' in f' {param_str} ':
                    raise ValueError(f'Potential SQL injection detected: {keyword}')
        
        return query_params


class SecurityMonitor:
    """Monitor and log security events"""
    
    @staticmethod
    def log_security_event(event_type, username=None, details=None):
        """Log security-related events"""
        try:
            log = SecurityLog(
                event_type=event_type,
                username=username,
                ip_address=request.remote_addr,
                details=details
            )
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to log security event: {e}")
    
    @staticmethod
    def record_login_attempt(username, success, user_agent=None):
        """Record login attempt for rate limiting and monitoring"""
        try:
            attempt = LoginAttempt(
                username=username,
                ip_address=request.remote_addr,
                success=success,
                user_agent=user_agent
            )
            db.session.add(attempt)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Failed to record login attempt: {e}")
    
    @staticmethod
    def check_rate_limit(username, max_attempts=5, lockout_minutes=5):
        """Check if user has exceeded login attempts"""
        try:
            lockout_time = datetime.utcnow() - timedelta(minutes=lockout_minutes)
            
            recent_attempts = LoginAttempt.query.filter(
                LoginAttempt.username == username,
                LoginAttempt.attempt_time > lockout_time,
                LoginAttempt.success == False
            ).count()
            
            return recent_attempts >= max_attempts
        except Exception as e:
            current_app.logger.error(f"Failed to check rate limit: {e}")
            return False
    
    @staticmethod
    def get_failed_attempts_count(username, minutes=5):
        """Get count of failed login attempts in last X minutes"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(minutes=minutes)
            
            count = LoginAttempt.query.filter(
                LoginAttempt.username == username,
                LoginAttempt.attempt_time > cutoff_time,
                LoginAttempt.success == False
            ).count()
            
            return count
        except Exception as e:
            current_app.logger.error(f"Failed to get failed attempts count: {e}")
            return 0


class SessionSecurity:
    """Manage session security"""
    
    @staticmethod
    def validate_session():
        """Validate current session"""
        # Check session age
        # Check IP consistency
        # Check user agent consistency
        pass
    
    @staticmethod
    def rotate_session():
        """Rotate session ID for security"""
        pass