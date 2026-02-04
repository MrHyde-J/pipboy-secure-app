# 🎮 Pip-Boy 3000 Secure Web Application

![Pip-Boy Interface](https://img.shields.io/badge/Interface-PipBoy-green)
![Flask](https://img.shields.io/badge/Framework-Flask-red)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Security](https://img.shields.io/badge/Security-A%2B-brightgreen)

A secure web application built with Flask featuring a **Fallout Pip-Boy 3000 interface**. This application demonstrates comprehensive web security practices with an engaging retro-futuristic user interface.

## ✨ Features

### 🔐 Core Security Features (Mandatory)
- ✅ **User Registration & Login System**
- ✅ **Password Hashing** (PBKDF2-SHA256 with salt)
- ✅ **Role-Based Access Control** (Admin/User)
- ✅ **Protected Routes** (Cannot access via URL directly)
- ✅ **Input Validation** (Prevents SQL Injection & XSS)

### 🎯 Chosen Feature: Password Strength Meter
- ✅ Real-time password analysis
- ✅ Visual strength indicator with Pip-Boy theme
- ✅ Detailed feedback and suggestions
- ✅ Common password detection
- ✅ Pattern recognition

### 🖥️ Pip-Boy Interface Features
- ✅ Authentic CRT scanline effects
- ✅ Phosphor glow and screen curvature
- ✅ Geiger counter animation
- ✅ Radio tuner interface
- ✅ Holotape-style cards
- ✅ Inventory-style lists
- ✅ Authentic sound effects

## 🏗️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Python 3.8+, Flask 3.0.0 |
| **Database** | SQLite (Development) |
| **Security** | Werkzeug, Flask-Login, Bleach |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Theme** | Fallout Pip-Boy 3000 from New Vegas |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation
```bash
# 1. Clone repository
git clone https://github.com/yourusername/pipboy-secure-app.git
cd pipboy-secure-app

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python main.py

# 5. Open browser
# http://localhost:5000
