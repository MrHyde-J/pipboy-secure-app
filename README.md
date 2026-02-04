# Vault-Tec Secure Web Application

## Overview
A secure web application built with Flask, featuring a Fallout Pip-Boy 3000 interface theme. This application demonstrates comprehensive web security practices with an engaging retro-futuristic user interface.

## Features

### Core Security Features (Mandatory)
- ✅ User Registration & Login System
- ✅ Password Hashing (PBKDF2-SHA256 with salt)
- ✅ Role-Based Access Control (Admin/User)
- ✅ Protected Routes (Cannot access via URL directly)
- ✅ Input Validation (Prevents SQL Injection & XSS)

### Chosen Feature: Password Strength Meter
- ✅ Real-time password analysis
- ✅ Visual strength indicator with Pip-Boy theme
- ✅ Detailed feedback and suggestions
- ✅ Common password detection
- ✅ Pattern recognition

## Technology Stack
- **Backend**: Python 3.8+, Flask 3.0.0
- **Database**: SQLite (Development), PostgreSQL ready
- **Security**: Werkzeug, Flask-Login, Bleach
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Theme**: Fallout Pip-Boy 3000 from New Vegas

## Project Structure