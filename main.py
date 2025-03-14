import os
import sys
import subprocess
import importlib
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Set up logging with reduced verbosity
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

# Define Python dependencies
python_dependencies = {
    "fastapi": "fastapi",
    "uvicorn": "uvicorn"
}

def install_missing_dependencies():
    """Install missing Python dependencies efficiently."""
    missing = [pkg for pkg in python_dependencies if not is_package_installed(pkg)]
    
    if missing:
        logging.info(f"📦 Installing {len(missing)} missing dependencies...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-cache-dir"] + missing,
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        logging.info(f"✅ Installed missing dependencies: {', '.join(missing)}")
    else:
        logging.info("✅ All Python dependencies are installed!")

def is_package_installed(package_name):
    """Check if a package is installed."""
    try:
        importlib.import_module(python_dependencies[package_name])
        return True
    except ImportError:
        return False

def ensure_file_exists(filename, default_content=""):
    """Ensure a file exists, and create it if it doesn't."""
    if not os.path.exists(filename):
        try:
            with open(filename, "w") as file:
                file.write(default_content)
            logging.info(f"Created missing file: {filename}")
        except Exception as e:
            logging.error(f"⚠️ Error creating file {filename}: {e}")

def read_config(file="config.txt"):
    """Read configuration from environment variables or config file."""
    config = {
        "port": os.getenv("PORT", "5000"),
        "host": os.getenv("HOST", "127.0.0.1"),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO").upper(),
        "use_ssl": os.getenv("USE_SSL", "false").lower() == "true",
        "cert_file": os.getenv("CERT_FILE", "cert.pem"),
        "key_file": os.getenv("KEY_FILE", "key.pem"),
        "template_folder": os.getenv("TEMPLATE_FOLDER", "templates"),
        "static_folder": os.getenv("STATIC_FOLDER", "static"),
    }
    
    ensure_file_exists(file, "port:5000\n")
    
    try:
        with open(file, "r") as f:
            for line in f:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    config[key.strip()] = value.strip()
                    
        required_keys = ["port", "host"]
        for key in required_keys:
            if key not in config:
                raise ValueError(f"⚠️ Missing mandatory config key: {key}")
    except Exception as e:
        logging.error(f"⚠️ Error reading config file: {e}")
        raise
    
    return config

# Install dependencies before using them
install_missing_dependencies()

# Read configuration
config = read_config()
PORT = int(config.get("port", 5000))
DEBUG_MODE = config.get("debug", False)
HOST = config.get("host", "127.0.0.1")
TEMPLATE_FOLDER = config.get("template_folder", "templates")
STATIC_FOLDER = config.get("static_folder", "static")
LOG_LEVEL = config.get("log_level", "INFO").upper()
USE_SSL = config.get("use_ssl", False)
CERT_FILE = config.get("cert_file", "cert.pem")
KEY_FILE = config.get("key_file", "key.pem")

# Ensure necessary files and folders exist
ensure_file_exists(f"{TEMPLATE_FOLDER}/index.html", "<html><body><h1>Welcome to FastAPI</h1></body></html>")
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Update logging level dynamically
logging.getLogger().setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

# FastAPI app setup
app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory=STATIC_FOLDER), name="static")

@app.get("/")
async def home():
    """Serve the home page."""
    return FileResponse(f"{TEMPLATE_FOLDER}/index.html")

@app.get("/ServerBase")
async def about():
    return "This server is powered by ServerBase by SethJ152 on GitHub."

def run_fastapi_app():
    """Run the FastAPI web application."""
    try:
        logging.info(f"Starting FastAPI server on {HOST}:{PORT}...")
        if USE_SSL:
            subprocess.run([
                sys.executable, "-m", "uvicorn", "main:app", "--host", HOST, "--port", str(PORT),
                "--ssl-keyfile", KEY_FILE, "--ssl-certfile", CERT_FILE
            ], check=True)
        else:
            subprocess.run([
                sys.executable, "-m", "uvicorn", "main:app", "--host", HOST, "--port", str(PORT)
            ], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"⚠️ Error starting FastAPI server: {e}")
    except Exception as e:
        logging.error(f"⚠️ Unexpected error: {e}")

def main():
    """Main function to set up and run the FastAPI app."""
    logging.info("🚀 Starting setup process...")
    try:
        run_fastapi_app()
        logging.info("🎉 System Complete!")
    except Exception as e:
        logging.error(f"⚠️ System setup failed: {e}")

if __name__ == "__main__":
    main()
