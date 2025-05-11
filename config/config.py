import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, os.getenv('TOKEN_FILENAME'))
CREDENTIALS_PATH = os.path.join(BASE_DIR, os.getenv('CREDENTIALS_FILENAME'))
SCOPES = SCOPES = os.getenv("SCOPES").split(",")

SERVER = os.getenv('SERVER')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')
