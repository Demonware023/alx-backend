#!/usr/bin/env python3
"""
Flask app with a single route
"""

from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index() -> str:
    """
    Handles the index route and renders the index template.

    Returns:
        str: Rendered HTML template.
    """
    return render_template('0-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
