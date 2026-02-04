import re
from datetime import datetime

class PasswordStrengthMeter:
    def __init__(self):
        self.common_passwords = [
            'password', '123456', '12345678', '123456789', '12345',
            'qwerty', 'abc123', 'password1', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'football', 'baseball',
            'hello', 'master', 'sunshine', 'trustno1', 'superman'
        ]
    
    def calculate_strength(self, password):
        """Calculate password strength with detailed feedback"""
        score = 0
        feedback = []
        
        # Length check
        length = len(password)
        if length >= 8:
            score += 15
            if length >= 12:
                score += 10
                if length >= 16:
                    score += 10
            else:
                feedback.append("Consider longer sequence (12+ characters recommended)")
        else:
            feedback.append("INSUFFICIENT LENGTH: Minimum 8 characters required")
        
        # Character variety checks
        has_upper = re.search(r'[A-Z]', password)
        has_lower = re.search(r'[a-z]', password)
        has_digit = re.search(r'\d', password)
        has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
        
        if has_upper:
            score += 15
        else:
            feedback.append("Add UPPERCASE letters for enhanced security")
        
        if has_lower:
            score += 15
        else:
            feedback.append("Include lowercase letters for complexity")
        
        if has_digit:
            score += 15
        else:
            feedback.append("NUMERICAL VALUES recommended")
        
        if has_special:
            score += 20
        else:
            feedback.append("SPECIAL CHARACTERS advised for maximum security")
        
        # Character variety bonus
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        if char_types >= 3:
            score += 10
        if char_types == 4:
            score += 10
        
        # Dictionary and common password check
        password_lower = password.lower()
        if password_lower in self.common_passwords:
            score = max(10, score - 40)
            feedback.insert(0, "CRITICAL: Common password detected - HIGH RISK")
        
        # Check for keyboard patterns
        if self.has_keyboard_pattern(password_lower):
            score -= 15
            feedback.append("Keyboard pattern detected - avoid sequential keys")
        
        # Check for repeated characters
        if self.has_repeated_chars(password):
            score -= 10
            feedback.append("Repeated character patterns reduce security")
        
        # Check for personal info patterns (simplified)
        if re.search(r'\d{4}', password):  # Likely year
            score -= 5
            feedback.append("Avoid using years in passwords")
        
        # Entropy calculation (simplified)
        unique_chars = len(set(password))
        score += min(20, unique_chars * 2)
        
        # Final score clamping
        score = min(100, max(0, score))
        
        # Categorization with Pip-Boy theme
        if score >= 85:
            category = "STRONG // VAULT-TEC APPROVED"
            color = "#00FF00"
            status = "SECURE"
        elif score >= 70:
            category = "GOOD // SECURE"
            color = "#99FF33"
            status = "ACCEPTABLE"
        elif score >= 50:
            category = "MODERATE // ACCEPTABLE"
            color = "#FFFF00"
            status = "REVIEW RECOMMENDED"
        elif score >= 30:
            category = "WEAK // SECURITY RISK"
            color = "#FF9900"
            status = "UPGRADE ADVISED"
        else:
            category = "CRITICAL FAILURE"
            color = "#FF3300"
            status = "IMMEDIATE ACTION REQUIRED"
        
        # Generate timestamp and scan ID
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scan_id = f"SCAN-{datetime.now().timestamp():.0f}"
        
        # If no specific feedback, provide positive reinforcement
        if not feedback and score >= 70:
            feedback = ["Password meets all security requirements"]
        elif not feedback:
            feedback = ["Password requires improvement"]
        
        return {
            'score': score,
            'category': category,
            'color': color,
            'status': status,
            'feedback': feedback,
            'timestamp': timestamp,
            'scan_id': scan_id,
            'length': length,
            'has_upper': bool(has_upper),
            'has_lower': bool(has_lower),
            'has_digit': bool(has_digit),
            'has_special': bool(has_special),
            'unique_chars': unique_chars
        }
    
    def has_keyboard_pattern(self, password):
        """Check for keyboard sequential patterns"""
        keyboard_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
            '1234567890'
        ]
        
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                sequence = row[i:i+3]
                if sequence in password or sequence[::-1] in password:
                    return True
        
        return False
    
    def has_repeated_chars(self, password):
        """Check for repeated character patterns"""
        return bool(re.search(r'(.)\1{2,}', password))
    
    def get_detailed_analysis(self, password):
        """Get detailed password analysis"""
        strength = self.calculate_strength(password)
        
        # Add time to crack estimates (simplified)
        if strength['score'] >= 85:
            time_to_crack = "CENTURIES"
        elif strength['score'] >= 70:
            time_to_crack = "DECADES"
        elif strength['score'] >= 50:
            time_to_crack = "YEARS"
        elif strength['score'] >= 30:
            time_to_crack = "MONTHS"
        else:
            time_to_crack = "SECONDS"
        
        strength['time_to_crack'] = time_to_crack
        strength['entropy_bits'] = self.calculate_entropy(password)
        
        return strength
    
    def calculate_entropy(self, password):
        """Calculate approximate entropy bits"""
        charset_size = 0
        if re.search(r'[a-z]', password):
            charset_size += 26
        if re.search(r'[A-Z]', password):
            charset_size += 26
        if re.search(r'\d', password):
            charset_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            charset_size += 32  # Approximate for special chars
        
        if charset_size == 0:
            return 0
        
        entropy_per_char = charset_size.bit_length()
        return len(password) * entropy_per_char
    
    def generate_strong_password(self, length=16):
        """Generate a strong password (optional feature)"""
        import random
        import string
        
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        while True:
            password = ''.join(random.choice(characters) for _ in range(length))
            if self.calculate_strength(password)['score'] >= 85:
                return password