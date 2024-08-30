#!/usr/bin/env python3
"""
Flask app with Babel for internationalization and language selection.
"""

from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)


class Config:
    """
    Configuration class for Flask-Babel.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def get_locale():
    """
    Determines the best match with supported languages based on
    the request's Accept-Language header or the locale parameter in the URL.

    Returns:
        str: The best match language code.
    """
    # Check if the locale parameter is in the request args and is supported
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale
    # Fall back to the best match based on the Accept-Language header
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index() -> str:
    """
    Handles the index route and renders the index template.

    Returns:
        str: Rendered HTML template.
    """
    return render_template('3-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
