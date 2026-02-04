// Password Strength Meter with Pip-Boy Theme
class PasswordStrengthMeter {
    constructor() {
        this.commonPasswords = new Set([
            'password', '123456', '12345678', '123456789', '12345',
            'qwerty', 'abc123', 'password1', 'admin', 'letmein',
            'welcome', 'monkey', 'dragon', 'football', 'baseball'
        ]);
        
        this.initializeElements();
        this.bindEvents();
    }

    initializeElements() {
        try {
            this.passwordInput = document.getElementById('password-input');
            this.meterBar = document.getElementById('meter-bar');
            this.meterGlow = document.getElementById('meter-glow');
            this.securityRating = document.getElementById('security-rating');
            this.scoreElement = document.getElementById('score');
            this.statusElement = document.getElementById('status');
            this.timestampElement = document.getElementById('timestamp');
            this.scanIdElement = document.getElementById('scan-id');
            this.feedbackList = document.getElementById('feedback-list');
        } catch (e) {
            console.log('Error initializing elements:', e);
        }
    }

    bindEvents() {
        if (this.passwordInput) {
            this.passwordInput.addEventListener('input', (e) => {
                this.analyzePassword(e.target.value);
            });
            
            // Real-time visual feedback
            this.passwordInput.addEventListener('keydown', (e) => {
                if (window.playSound) {
                    try {
                        window.playSound('click');
                    } catch (soundError) {
                        // Ignore sound errors
                    }
                }
            });
        }
    }

    analyzePassword(password) {
        if (!password) {
            this.resetDisplay();
            return;
        }

        const analysis = this.calculateStrength(password);
        this.updateDisplay(analysis);
        
        // Send to backend for additional analysis
        this.sendToBackend(password).catch(e => {
            // Silently fail backend analysis
            console.log('Backend analysis failed:', e);
        });
    }

    calculateStrength(password) {
        if (typeof password !== 'string') {
            return this.getDefaultResult();
        }
        
        let score = 0;
        const feedback = [];
        const timestamp = new Date().toLocaleString();
        const scanId = `SCAN-${Date.now().toString(36).toUpperCase()}`;

        // Length check
        const length = password.length;
        if (length >= 8) {
            score += 20;
            if (length >= 12) score += 10;
            if (length >= 16) score += 10;
        } else {
            feedback.push("INSUFFICIENT LENGTH: Minimum 8 characters required");
        }

        // Character variety
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasSpecial = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        if (hasUpperCase) {
            score += 15;
        } else {
            feedback.push("ADD UPPERCASE LETTERS for enhanced security");
        }

        if (hasLowerCase) {
            score += 15;
        } else {
            feedback.push("Include lowercase letters for complexity");
        }

        if (hasNumbers) {
            score += 15;
        } else {
            feedback.push("NUMERICAL VALUES recommended");
        }

        if (hasSpecial) {
            score += 20;
        } else {
            feedback.push("SPECIAL CHARACTERS advised for maximum security");
        }

        // Dictionary check
        if (this.commonPasswords.has(password.toLowerCase())) {
            score = Math.max(10, score - 40);
            feedback.unshift("CRITICAL: Common password detected - HIGH RISK");
        }

        // Entropy calculation
        try {
            const uniqueChars = new Set(password).size;
            score += Math.min(20, uniqueChars * 2);
        } catch (e) {
            // Ignore entropy calculation errors
        }

        // Pattern detection (simplified)
        if (/(.)\1{2,}/.test(password)) {
            score -= 15;
            feedback.push("Avoid repeated character patterns");
        }

        if (/^[0-9]+$/.test(password) || /^[a-zA-Z]+$/.test(password)) {
            score -= 20;
            feedback.push("Mixed character types required");
        }

        // Sequential patterns
        if (this.hasSequentialChars(password)) {
            score -= 10;
            feedback.push("Sequential patterns detected");
        }

        // Cap score
        score = Math.max(0, Math.min(100, Math.round(score)));

        // Determine category
        let category, color;
        if (score >= 85) {
            category = "STRONG // VAULT-TEC APPROVED";
            color = "#00FF00";
        } else if (score >= 70) {
            category = "GOOD // SECURE";
            color = "#99FF33";
        } else if (score >= 50) {
            category = "MODERATE // ACCEPTABLE";
            color = "#FFFF00";
        } else if (score >= 30) {
            category = "WEAK // SECURITY RISK";
            color = "#FF9900";
        } else {
            category = "CRITICAL FAILURE";
            color = "#FF3300";
        }

        return {
            score,
            category,
            color,
            feedback: feedback.length ? feedback : ["PASSWORD MEETS MINIMUM REQUIREMENTS"],
            timestamp,
            scanId
        };
    }

    hasSequentialChars(str) {
        if (typeof str !== 'string') return false;
        
        const sequences = [
            'abcdefghijklmnopqrstuvwxyz',
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm',
            '0123456789'
        ];
        
        const testStr = str.toLowerCase();
        
        for (let seq of sequences) {
            for (let i = 0; i <= seq.length - 3; i++) {
                const sequence = seq.substr(i, 3);
                if (testStr.includes(sequence) || testStr.includes(sequence.split('').reverse().join(''))) {
                    return true;
                }
            }
        }
        return false;
    }

    getDefaultResult() {
        return {
            score: 0,
            category: "ANALYZING...",
            color: "#888888",
            feedback: ["Enter password to begin analysis..."],
            timestamp: new Date().toLocaleString(),
            scanId: "SCAN-INIT"
        };
    }

    updateDisplay(analysis) {
        if (!analysis) return;
        
        try {
            // Update meter
            if (this.meterBar) {
                this.meterBar.style.width = `${analysis.score}%`;
                this.meterBar.style.backgroundColor = analysis.color;
            }
            
            if (this.meterGlow) {
                this.meterGlow.style.boxShadow = `inset 0 0 10px ${analysis.color}`;
            }

            // Update text elements
            const updates = {
                'securityRating': analysis.category,
                'scoreElement': `${analysis.score}/100`,
                'statusElement': analysis.score >= 70 ? "SECURE" : "REVIEW REQUIRED",
                'timestampElement': analysis.timestamp,
                'scanIdElement': `SCAN-ID: ${analysis.scanId}`
            };
            
            Object.entries(updates).forEach(([elementName, value]) => {
                const element = this[elementName];
                if (element) {
                    element.textContent = value;
                    if (elementName === 'securityRating' || elementName === 'scoreElement' || elementName === 'statusElement') {
                        element.style.color = analysis.color;
                    }
                }
            });

            // Update feedback list
            if (this.feedbackList) {
                this.feedbackList.innerHTML = '';
                if (Array.isArray(analysis.feedback)) {
                    analysis.feedback.forEach(item => {
                        const li = document.createElement('li');
                        li.textContent = item;
                        li.style.color = analysis.score >= 70 ? '#88FF88' : '#FF8888';
                        this.feedbackList.appendChild(li);
                    });
                }
            }

            // Add visual effects
            if (this.meterBar) {
                if (analysis.score >= 85) {
                    this.meterBar.classList.add('glowing');
                } else {
                    this.meterBar.classList.remove('glowing');
                }
            }
        } catch (e) {
            console.log('Error updating display:', e);
        }
    }

    resetDisplay() {
        try {
            if (this.meterBar) {
                this.meterBar.style.width = '0%';
                this.meterBar.classList.remove('glowing');
            }
            
            if (this.meterGlow) {
                this.meterGlow.style.boxShadow = 'none';
            }
            
            const elements = [
                this.securityRating,
                this.scoreElement,
                this.statusElement,
                this.timestampElement,
                this.scanIdElement
            ];
            
            elements.forEach(element => {
                if (element) {
                    element.textContent = element === this.scoreElement ? '0/100' : '---';
                    element.style.color = '';
                }
            });
            
            if (this.feedbackList) {
                this.feedbackList.innerHTML = '<li>Enter password to begin analysis...</li>';
            }
        } catch (e) {
            console.log('Error resetting display:', e);
        }
    }

    async sendToBackend(password) {
        if (!password || typeof password !== 'string') {
            return;
        }
        
        try {
            const response = await fetch('/api/check-password', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ password: password })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            
            // Optional: Merge backend analysis with frontend
            if (data && typeof data.score === 'number') {
                // Could merge results here if needed
                console.log('Backend analysis received');
            }
        } catch (error) {
            // Silently fail - frontend analysis is sufficient
            throw error;
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    try {
        const meter = new PasswordStrengthMeter();
        
        // Make available globally for manual calls
        window.passwordMeter = meter;
        
        // Initialize with empty password
        meter.resetDisplay();
        
        // Also initialize password toggles if they exist
        const passwordInputs = document.querySelectorAll('input[type="password"]');
        passwordInputs.forEach(input => {
            const parent = input.parentElement;
            if (parent && !parent.querySelector('.password-toggle')) {
                const toggle = document.createElement('button');
                toggle.type = 'button';
                toggle.className = 'password-toggle';
                toggle.textContent = '👁️';
                toggle.addEventListener('click', function() {
                    const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                    input.setAttribute('type', type);
                    this.textContent = type === 'password' ? '👁️' : '👁️‍🗨️';
                    if (window.playSound) {
                        window.playSound('click');
                    }
                });
                parent.appendChild(toggle);
            }
        });
        
    } catch (e) {
        console.log('Error initializing password meter:', e);
    }
});