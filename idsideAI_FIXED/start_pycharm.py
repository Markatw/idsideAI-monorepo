#!/usr/bin/env python3
"""
PyCharm Startup Helper
======================
Ensures everything is ready for PyCharm development
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Ensure Python 3.11+ is available"""
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ Core dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Create .env file if it doesn't exist"""
    env_path = Path(".env")
    if not env_path.exists():
        print("📝 Creating .env file...")
        with open(env_path, "w") as f:
            f.write("""# IDECIDE AI Configuration
DATABASE_URL=sqlite+aiosqlite:///./idsideai.db
OPENAI_API_KEY=${OPENAI_API_KEY:-}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT:-}
AZURE_OPENAI_KEY=${AZURE_OPENAI_KEY:-}
ALLOW_FAKE_PROVIDER=true
""")
        print("✅ .env file created")
    else:
        print("✅ .env file exists")

def setup_database():
    """Initialize database if needed"""
    db_path = Path("idsideai.db")
    if not db_path.exists():
        print("🗄️ Setting up database...")
        try:
            subprocess.run([sys.executable, "setup.py"], check=True)
            print("✅ Database initialized")
        except subprocess.CalledProcessError:
            print("⚠️ Database setup failed, but application may still work")
    else:
        print("✅ Database exists")

def check_pycharm_config():
    """Verify PyCharm configuration exists"""
    idea_path = Path(".idea")
    if idea_path.exists():
        print("✅ PyCharm configuration ready")
        return True
    else:
        print("⚠️ PyCharm configuration missing (will be created on first open)")
        return False

def main():
    """Main startup check"""
    print("🚀 idsideAI PyCharm Startup Check")
    print("=" * 40)
    
    checks = [
        check_python_version(),
        check_dependencies(),
    ]
    
    # Setup tasks
    setup_environment()
    setup_database()
    check_pycharm_config()
    
    print("\n" + "=" * 40)
    if all(checks):
        print("🎉 Ready for PyCharm development!")
        print("\n📋 Next steps:")
        print("1. Open this folder in PyCharm")
        print("2. Select 'Run idsideAI Application' configuration")
        print("3. Click the Run button ▶️")
        print("4. Access application at http://localhost:8000")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
