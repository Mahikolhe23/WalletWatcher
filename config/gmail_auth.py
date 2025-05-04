from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

SCOPES = [
    'https://mail.google.com/',
    'openid',                   
    'https://www.googleapis.com/auth/userinfo.email',  
    'https://www.googleapis.com/auth/userinfo.profile' 
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'token.pickle')
CREDENTIALS_PATH = os.path.join(BASE_DIR, 'secret.json')

def get_token():
    creds = None
    if os.path.exists(TOKEN_PATH) :
        with open(TOKEN_PATH,'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=8080)
            
            with open(TOKEN_PATH,'wb') as token:
                pickle.dump(creds, token)
    return creds 

