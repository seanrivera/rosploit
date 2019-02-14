# app/__init__.py
from flask import Flask

# Load the views
from demo.app import views

# Initialize the app
demo: Flask = Flask(__name__, instance_relative_config=True, template_folder="app/templates",
                    static_folder="app/static")


# Load the config file
demo.config.from_object('demo.config')
global NMAP_DATA_DIR
