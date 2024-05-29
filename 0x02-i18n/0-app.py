#!/usr/bin/env python3
"""
flask api
"""
from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def index():
    """html page output"""
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run()
