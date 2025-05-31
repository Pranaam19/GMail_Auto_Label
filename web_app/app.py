# web_app/app.py
from flask import Flask, render_template, redirect, url_for, request, session
import os
from . import gmail_auth # Assuming gmail_auth.py is in the same directory
from . import processing_logic
from flask import jsonify # For potential future XHR requests

app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for session management, though state validation is minimal here

@app.route('/')
def home():
    authenticated = gmail_auth.is_authenticated()
    return render_template('index.html', message='Welcome to GMail Auto Label!', authenticated=authenticated, results=None)

@app.route('/login')
def login():
    try:
        authorization_url, state = gmail_auth.get_authorization_url()
        # For simplicity in single user, not formally using state for CSRF here,
        # but it's returned by flow.authorization_url
        # session['oauth_state'] = state
        return redirect(authorization_url)
    except FileNotFoundError as e:
        return str(e) + "<br><a href='/'>Home</a>", 500


@app.route('/oauth2callback')
def oauth2callback():
    # For robustness, validate state: if 'state' not in session or session['state'] != request.args.get('state'): abort(400)
    try:
        gmail_auth.exchange_code_for_credentials(request.url)
        return redirect(url_for('home'))
    except Exception as e:
        return f"Error during OAuth callback: {e} <br><a href='/'>Home</a>", 500

@app.route('/logout')
def logout():
    gmail_auth.logout()
    return redirect(url_for('home'))

@app.route('/process')
def process_emails_route():
    if not gmail_auth.is_authenticated():
        return redirect(url_for('login'))

    # For simplicity now, show results on a new page or part of index.
    # Later, this could be an async task.
    results = processing_logic.process_user_emails()
    # return render_template('index.html', authenticated=True, results=results, message='Email Processing Complete')
    # For now, let's just update index.html to show results.
    # The button on index.html will be a GET request to this for now.
    return render_template('results.html', results=results, authenticated=True, message='Email Processing Status')

@app.errorhandler(500)
def internal_server_error(e):
    # Optionally log the error e here if more detailed logging is needed
    return render_template('500.html', error=e), 500

if __name__ == '__main__':
    # Important for OAuth: Flask dev server needs to run on http, not https, unless certs are set up.
    # Also, Google Cloud Console redirect URI must match exactly (e.g. http://localhost:5000/oauth2callback)
    app.run(debug=True, port=5000)
