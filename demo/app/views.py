# views.py

from flask import render_template

from demo import demo


@demo.route('/')
def index():
    return render_template("index.html")


@demo.route('/about')
def about():
    return render_template("about.html")
