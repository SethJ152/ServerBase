import os
import sys
import subprocess

# List of 150 Python dependencies
python_dependencies = [
    "flask",                # 1. Web framework
    "pyjwt",                # 2. JSON Web Token
    "werkzeug",             # 3. WSGI utility library
    "flask-session",        # 4. Session management
    "flask-socketio",       # 5. WebSockets support
    "flask-cors",           # 6. Cross-origin resource sharing
    "numpy",                # 7. Array and numerical computing
    "scipy",                # 8. Scientific computing
    "pandas",               # 9. Data manipulation and analysis
    "matplotlib",           # 10. Plotting library
    "seaborn",              # 11. Statistical data visualization
    "tensorflow",           # 12. Deep learning framework
    "scikit-learn",         # 13. Machine learning
    "requests",             # 14. HTTP library
    "beautifulsoup4",       # 15. HTML/XML parsing
    "pillow",               # 16. Imaging library
    "pytest",               # 17. Testing framework
    "pytest-cov",           # 18. Test coverage reporting
    "flask-sqlalchemy",     # 19. ORM for Flask
    "flask-migrate",        # 20. Database migrations
    "flask-login",          # 21. User session management
    "flask-mail",           # 22. Email support for Flask
    "flask-wtf",            # 23. WTForms integration
    "flask-restful",        # 24. REST API support
    "flask-admin",          # 25. Admin interface
    "flask-bcrypt",         # 26. Password hashing
    "flask-caching",        # 27. Caching support
    "flask-jwt-extended",   # 28. JWT support for Flask
    "sqlalchemy",           # 29. Database toolkit
    "sqlalchemy-utils",     # 30. Extra utilities for SQLAlchemy
    "gunicorn",             # 31. WSGI server
    "black",                # 32. Code formatter
    "autopep8",             # 33. PEP8 auto-formatter
    "isort",                # 34. Import sorter
    "requests-oauthlib",    # 35. OAuth support for Requests
    "pyyaml",               # 36. YAML parsing
    "cryptography",         # 37. Cryptographic recipes and primitives
    "pyodbc",               # 38. ODBC database connector
    "sqlalchemy-migrate",   # 39. Database migrations with SQLAlchemy
    "pyttsx3",              # 40. Text-to-speech conversion
    "psycopg2",             # 41. PostgreSQL adapter
    "pymongo",              # 42. MongoDB driver
    "sqlite3",              # 43. SQLite (bundled with Python)
    "tkinter",              # 44. GUI toolkit (bundled with Python)
    "pyqt5",                # 45. Cross-platform GUI toolkit
    "jupyter",              # 46. Jupyter notebooks
    "notebook",             # 47. Jupyter Notebook server
    "ipython",              # 48. Enhanced interactive shell
    "ipykernel",            # 49. IPython kernel for Jupyter
    "voila",                # 50. Turn notebooks into standalone web apps
    "dash",                 # 51. Analytical web apps
    "plotly",               # 52. Interactive graphing library
    "bokeh",                # 53. Interactive visualization
    "holoviews",            # 54. Simplify data visualization
    "panel",                # 55. Dashboarding tool
    "streamlit",            # 56. Rapid app development
    "fastapi",              # 57. High-performance API framework
    "uvicorn",              # 58. ASGI server for FastAPI
    "aiohttp",              # 59. Asynchronous HTTP client/server
    "sanic",                # 60. Async web framework
    "tornado",              # 61. Scalable web server and framework
    "celery",               # 62. Distributed task queue
    "redis",                # 63. Redis client
    "rq",                   # 64. Simple job queues
    "kombu",                # 65. Messaging library (used with Celery)
    "boto3",                # 66. AWS SDK for Python
    "botocore",             # 67. Low-level AWS service access
    "s3transfer",           # 68. S3 transfers library
    "elasticsearch",        # 69. Elasticsearch client
    "opensearch-py",        # 70. OpenSearch client
    "pyopenssl",            # 71. SSL/TLS support
    "paramiko",             # 72. SSH library
    "fabric",               # 73. Remote command execution
    "invoke",               # 74. Task execution tool
    "scapy",                # 75. Packet manipulation tool
    "pexpect",              # 76. Automate interactive applications
    "scrapyd",              # 77. Scrapyd server for Scrapy
    "scrapy",               # 78. Web scraping framework
    "newspaper3k",          # 79. News article extraction
    "fuzzywuzzy",           # 80. Fuzzy string matching
    "rapidfuzz",            # 81. Fast fuzzy matching
    "textblob",             # 82. Simplified NLP
    "nltk",                 # 83. Natural language toolkit
    "spacy",                # 84. Industrial-strength NLP
    "gensim",               # 85. Topic modeling
    "transformers",         # 86. State-of-the-art NLP
    "sentence-transformers",# 87. Sentence embeddings
    "flair",                # 88. NLP library by Zalando
    "allennlp",             # 89. NLP research library
    "opencv-python",        # 90. OpenCV bindings for Python
    "dlib",                 # 91. Machine learning toolkit (face detection, etc.)
    "mediapipe",            # 92. Cross-platform ML solutions
    "moviepy",              # 93. Video editing
    "imageio",              # 94. Reading/writing image data
    "pydub",                # 95. Audio manipulation
    "librosa",              # 96. Audio analysis
    "soundfile",            # 97. Audio I/O library
    "torchaudio",           # 98. Audio support for PyTorch
    "torch",                # 99. PyTorch deep learning framework
    "torchvision",          # 100. Computer vision for PyTorch
    "pytorch-lightning",    # 101. PyTorch training framework
    "timm",                 # 102. Image models for PyTorch
    "xgboost",              # 103. Gradient boosting framework
    "lightgbm",             # 104. Light gradient boosting
    "catboost",             # 105. Gradient boosting with categorical features
    "mlflow",               # 106. Machine learning lifecycle management
    "wandb",                # 107. Experiment tracking
    "optuna",               # 108. Hyperparameter optimization
    "hyperopt",             # 109. Distributed hyperparameter optimization
    "scikit-optimize",      # 110. Sequential model-based optimization
    "dask",                 # 111. Parallel computing with arrays/dataframes
    "pyspark",              # 112. Spark Python API
    "petastorm",            # 113. Data access for deep learning on Spark
    "prefect",              # 114. Workflow orchestration
    "airflow",              # 115. Workflow automation and scheduling
    "luigi",                # 116. Pipeline management
    "kedro",                # 117. Data and ML pipelines
    "great_expectations",   # 118. Data validation
    "pyarrow",              # 119. Cross-language development platform for columnar data
    "fastparquet",          # 120. Parquet file reader/writer
    "h5py",                 # 121. HDF5 for Python
    "tables",               # 122. Hierarchical datasets in Python
    "netCDF4",              # 123. Scientific data format
    "rasterio",             # 124. Geospatial raster data
    "geopandas",            # 125. Geospatial data analysis
    "shapely",              # 126. Manipulation and analysis of planar geometric objects
    "folium",               # 127. Mapping library
    "plotly-express",       # 128. Simplified Plotly API
    "pyecharts",            # 129. Interactive charts
    "altair",               # 130. Declarative statistical visualization
    "vega_datasets",        # 131. Sample datasets for Vega/Altair
    "streamlit-aggrid",     # 132. Grid component for Streamlit
    "dash-bootstrap-components", # 133. Bootstrap components for Dash
    "dash-core-components", # 134. Core Dash components
    "dash-html-components", # 135. HTML components for Dash
    "dash-daq",             # 136. Dash data acquisition components
    "pydantic",             # 137. Data validation and settings management
    "marshmallow",          # 138. Object serialization/deserialization
    "cerberus",             # 139. Data validation library
    "voluptuous",           # 140. Validation library
    "fastjsonschema",       # 141. Fast JSON schema validation
    "pytest-mock",          # 142. Pytest plugin for mocking
    "hypothesis",           # 143. Property-based testing
    "tox",                  # 144. Automated testing in multiple environments
    "coverage",             # 145. Code coverage tool
    "nbconvert",            # 146. Jupyter Notebook conversion
    "jinja2",               # 147. Templating engine
    "markupsafe",           # 148. Safely handle strings in Jinja2
    "itsdangerous",         # 149. Data signing for Flask
    "python-dotenv"         # 150. Load environment variables from .env files
]

def install_python_dependencies():
    """
    Install the required Python packages using pip with --break-system-packages,
    trying apt first, then falling back to pip.
    Output is suppressed.
    """
    for package in python_dependencies:
        # Try apt first
        try:
            print(package)
            subprocess.run(["sudo", "apt", "install", "-y", package],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            # Fall back to pip if apt fails
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package, "--break-system-packages"],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError as e:
                pass

def install_system_dependencies():
    """
    Installs system dependencies using apt without displaying messages.
    """
    system_dependencies = [
        "sqlite3",
        "libsqlite3-dev",
        "python3-tk",
        "build-essential",
        "python3-dev"
    ]
    try:
        if sys.platform.startswith("linux"):
            subprocess.run(["sudo", "apt", "update"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["sudo", "apt", "install", "-y"] + system_dependencies,
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif sys.platform == "darwin":
            subprocess.run(["brew", "install", "sqlite"],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"System dependency installation skipped or failed: {e}")

def main():
    print("🚀 Starting dependency installation...\n")

    # Install system dependencies
    install_system_dependencies()

    # Install Python dependencies (150 packages)
    install_python_dependencies()

    print("\n🎉 Setup complete! You can now run your Flask app.")

if __name__ == "__main__":
    main()

