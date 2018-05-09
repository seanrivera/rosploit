# app/__init__.py
from flask import Flask

# Initialize the app
demo: Flask = Flask(__name__, instance_relative_config=True, template_folder="app/templates")

# Load the views
from demo.app import views

# Load the config file
demo.config.from_object('demo.config')
global NMAP_DATA_DIR
