import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from config.config import BASE_DIR, CREDENTIALS_PATH, SCOPES
from dotenv import load_dotenv

load_dotenv()

def get_token(user_name):
    USER_PATH = f'{BASE_DIR}/tokens/{user_name}/'
    if not os.path.exists(USER_PATH) :
        os.mkdir(USER_PATH)

    TOKEN_PATH = f'{USER_PATH}/{os.getenv('TOKEN_FILENAME')}'
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

