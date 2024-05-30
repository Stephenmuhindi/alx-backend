#!/usr/bin/env python3
"""
Flask application demonstrating internationalization (i18n) and localization (l10n) features.

- Supports user-defined locale and timezone preferences.
- Employs Flask-Babel for language and timezone handling.
"""

from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel, format_datetime

# Application configuration
class Config:
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# Sample user data with locale and timezone information
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    # ... (more users)
}


def get_user(user_id: int) -> Union[Dict, None]:
    """Retrieves user information by ID."""
    return users.get(user_id)


@babel.localeselector
def get_locale():
    """Determines the user's preferred locale based on various sources."""
    options = [
        request.args.get('locale'),  # User-specified locale from URL query string
        g.user.get('locale') if g.user else None,  # User's locale preference (if logged in)
        request.accept_languages.best_match(app.config['LANGUAGES']),  # Browser's preferred language
        Config.BABEL_DEFAULT_LOCALE,  # Default application locale
    ]
    return next((o for o in options if o and o in Config.LANGUAGES), None)


@babel.timezoneselector
def get_timezone():
    """Determines the user's preferred timezone based on various sources."""
    user_tz = request.args.get('timezone') or g.user.get('timezone')  # User-specified timezone
    try:
        return pytz.timezone(user_tz).zone  # Validate and return valid timezone
    except pytz.exceptions.UnknownTimeZoneError:
        return app.config['BABEL_DEFAULT_TIMEZONE']  # Use default timezone


@app.before_request
def before_request():
    """Populates global context with user and current time information before each request."""
    g.user = get_user(request.args.get('login_as', 0))  # Retrieve user based on login ID
    g.time = format_datetime(datetime.datetime.now())  # Store current time


@app.route('/')
def index():
    """Renders the main application template."""
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

