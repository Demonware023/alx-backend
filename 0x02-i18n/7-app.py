#!/usr/bin/env python3
"""
Flask app with Babel for internationalization, language selection, and user login emulation.
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _
import pytz
from pytz.exceptions import UnknownTimeZoneError

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
    the request's locale parameter, user settings, Accept-Language header, or default locale.

    Returns:
        str: The best match language code.
    """
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']

    return request.accept_languages.best_match(app.config['LANGUAGES'])

@babel.timezoneselector
def get_timezone():
    """
    Determines the best match with supported timezones based on
    the request's timezone parameter, user settings, or default timezone.

    Returns:
        str: The best match timezone.
    """
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except UnknownTimeZoneError:
            pass

    if g.user and g.user['timezone']:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except UnknownTimeZoneError:
            pass

    return app.config['BABEL_DEFAULT_TIMEZONE']

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
