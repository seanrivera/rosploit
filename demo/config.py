# config.py
import os

# Enable Flask's debugging features. Should be False in production
DEBUG = True

# Allow flask to use session interfaces
SECRET_KEY = os.urandom(24)
