import os
import sys
import subprocess
import platform
import importlib
import logging

# Set up logging for better visibility
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Python dependencies with correct import names
python_dependencies = {
    "flask": "flask",
    "gunicorn": "gunicorn",
    "werkzeug": "werkzeug",
    "flask-cors": "flask_cors",
    "flask-session": "flask_session",
    "flask-socketio": "flask_socketio",
    "flask-sqlalchemy": "flask_sqlalchemy",
    "flask-migrate": "flask_migrate",
    "flask-login": "flask_login",
    "flask-jwt-extended": "flask_jwt_extended",
    "sqlalchemy": "sqlalchemy",
    "psycopg2": "psycopg2",
    "pymongo": "pymongo",
    "redis": "redis",
    "requests": "requests",
    "cryptography": "cryptography",
    "python-dotenv": "dotenv"
}

def is_package_installed(package_name):
    """
    Check if a Python package is installed using its correct import name.
    Returns True if installed, otherwise False.
    """
    import_name = python_dependencies.get(package_name)
    if not import_name:
        logging.error(f"Package {package_name} not found in dependency list.")
        return False
    try:
        importlib.import_module(import_name)
        return True
    except ImportError:
        return False

def install_python_dependencies():
    """
    Install missing Python dependencies.
    Displays progress dynamically and handles errors efficiently.
    """
    to_install = [pkg for pkg in python_dependencies if not is_package_installed(pkg)]
    total = len(to_install)

    if total == 0:
        logging.info("✅ All Python dependencies are already installed!")
        return

    logging.info(f"📦 Installing {total} missing dependencies...")
    for i, package in enumerate(to_install, 1):
        percent = int((i / total) * 100)
        sys.stdout.write(f"\rInstalling dependencies... {percent}%")
        sys.stdout.flush()
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            logging.info(f"Installed {package}")
        except subprocess.CalledProcessError as e:
            logging.warning(f"⚠️ Failed to install {package}: {e}")

    sys.stdout.write("\r✅ All required dependencies installed! 100%\n")

def install_system_dependencies():
    """
    Install system-level dependencies based on the operating system.
    """
    system_dependencies = {
        "Linux": ["sqlite3", "libsqlite3-dev", "python3-tk", "build-essential", "python3-dev"],
        "Darwin": ["sqlite"],
        "Windows": ["sqlite", "python-tk"]
    }

    os_type = platform.system()
    if os_type not in system_dependencies:
        logging.error(f"⚠️ Unsupported OS: {os_type}")
        return

    dependencies = system_dependencies[os_type]
    logging.info(f"Installing system dependencies for {os_type}...")

    try:
        if os_type == "Linux":
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y"] + dependencies, check=True)
        elif os_type == "Darwin":
            subprocess.run(["brew", "install"] + dependencies, check=True)
        elif os_type == "Windows":
            try:
                subprocess.run(["choco", "install", "-y"] + dependencies, check=True)
            except FileNotFoundError:
                try:
                    subprocess.run(["scoop", "install"] + dependencies, check=True)
                except FileNotFoundError:
                    logging.warning("⚠️ Chocolatey or Scoop not found. Please install dependencies manually.")
    except subprocess.CalledProcessError:
        logging.warning("⚠️ Failed to install system dependencies.")

def verify_installed_packages():
    """
    Verify that all required Python packages are correctly installed.
    """
    logging.info("\n🔧 Verifying installed packages...")
    for package, import_name in python_dependencies.items():
        if not is_package_installed(package):
            logging.warning(f"⚠️ {package} ({import_name}) is not installed.")
        else:
            logging.info(f"✅ {package} is installed.")

def setup_flask_app():
    """
    Sets up and runs the Flask web application.
    """
    try:
        from flask import Flask, render_template

        app = Flask(__name__)

        # Define a route for the homepage
        @app.route("/")
        def home():
            return render_template("index.html")

        # Run the app
        logging.info("Starting Flask server...")
        app.run(debug=True)
    except Exception as e:
        logging.error(f"⚠️ Error starting Flask server: {e}")

def main():
    """
    Main setup function to install dependencies and start the application.
    """
    logging.info("🚀 Starting setup process...\n")

    # Install system dependencies
    install_system_dependencies()

    # Install Python dependencies
    install_python_dependencies()

    # Verify installed Python packages
    verify_installed_packages()

    # Set up and run Flask app
    setup_flask_app()

    logging.info("\n🎉 System Complete!")

if __name__ == "__main__":
    main()
