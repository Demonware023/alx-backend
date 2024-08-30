#!/usr/bin/env python3
"""
Flask app with Babel for internationalization, language selection, and user login emulation.
"""

from flask import Flask, render_template, request, g
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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

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

def get_user() -> dict:
    """
    Returns a user dictionary based on the login_as URL parameter.
    
    Returns:
        dict or None: The user dictionary if ID is valid, else None.
    """
    user_id = request.args.get('login_as', type=int)
    return users.get(user_id, None)

@app.before_request
def before_request():
    """
    Set the global g.user based on the login_as URL parameter.
    """
    g.user = get_user()

@app.route('/')
def index() -> str:
    """
    Handles the index route and renders the index template.
    
    Returns:
        str: Rendered HTML template.
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
