#!/usr/bin/env python3
"""
Setup script for Vault-Tec Secure Web Application
"""

import os
import sys
import subprocess

def run_command(cmd, description):
    print(f"\n// {description} //")
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✓ {description} completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e}")
        sys.exit(1)

def main():
    print("""
    ╔══════════════════════════════════════════════╗
    ║   VAULT-TEC SECURE SYSTEM SETUP             ║
    ║   Initializing Pip-Boy 3000 Interface       ║
    ╚══════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("✗ Python 3.8 or higher is required")
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists('venv'):
        run_command('python -m venv venv', 'Creating virtual environment')
    
    # Activate virtual environment and install dependencies
    if os.name == 'nt':  # Windows
        activate_cmd = 'venv\\Scripts\\activate && pip install -r requirements.txt'
    else:  # Unix/Linux/Mac
        activate_cmd = 'source venv/bin/activate && pip install -r requirements.txt'
    
    run_command(activate_cmd, 'Installing dependencies')
    
    print("\n" + "="*50)
    print("SETUP COMPLETE!")
    print("="*50)
    print("\nTo run the application:")
    print("1. Activate virtual environment:")
    print("   Windows: venv\\Scripts\\activate")
    print("   Mac/Linux: source venv/bin/activate")
    print("2. Run: python app.py")
    print("3. Open: http://localhost:5000")
    print("\nDefault accounts:")
    print("   Admin: vault_admin / Vault-Tec2077!")
    print("   User: wastelander / NCR!2024")
    print("\n// VAULT-TEC WELCOMES YOU //")

if __name__ == '__main__':
    main()