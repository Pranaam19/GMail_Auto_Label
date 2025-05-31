# web_app/gmail_auth.py
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# Path to store the token and credentials files
TOKEN_PATH = os.path.join(os.path.dirname(__file__), 'token.json')
CREDENTIALS_PATH = os.path.join(os.path.dirname(__file__), 'credentials.json')
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
REDIRECT_URI = 'http://localhost:5000/oauth2callback' # Ensure this matches your Flask app's URL and Google Cloud Console config

def build_flow():
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(
            "credentials.json not found. Please download it from Google Cloud Console "
            "and place it in the 'web_app' directory."
        )
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    return flow

def get_authorization_url():
    flow = build_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    # Store state in session for later validation if implementing for multi-user or more robust security
    # For single user, direct use is simpler for now.
    return authorization_url, state

def exchange_code_for_credentials(authorization_response_url):
    flow = build_flow()
    flow.fetch_token(authorization_response=authorization_response_url)
    creds = flow.credentials
    with open(TOKEN_PATH, 'w') as token_file:
        token_file.write(creds.to_json())
    return creds

def get_gmail_service():
    creds = None
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, 'w') as token_file: # Save refreshed token
                    token_file.write(creds.to_json())
            except Exception as e:
                # If refresh fails, token is likely invalid, user needs to re-authenticate
                print(f"Error refreshing token: {e}")
                if os.path.exists(TOKEN_PATH):
                     os.remove(TOKEN_PATH) # Remove invalid token
                return None # Indicate failure or need for re-auth
        else:
            # No valid token, user needs to authenticate
            return None

    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return None

def is_authenticated():
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if creds and creds.valid:
            return True
        elif creds and creds.expired and creds.refresh_token:
            # Try to refresh to see if it's still valid
            try:
                creds.refresh(Request())
                with open(TOKEN_PATH, 'w') as token_file:
                    token_file.write(creds.to_json())
                return True
            except Exception:
                return False # Refresh failed
    return False

def logout():
    if os.path.exists(TOKEN_PATH):
        os.remove(TOKEN_PATH)
