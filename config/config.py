import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = f'{BASE_DIR}/secrets/{os.getenv('CREDENTIALS_FILENAME')}'
SCOPES = SCOPES = os.getenv("SCOPES").split(",")

SERVER = os.getenv('SERVER')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DRIVER = os.getenv('DRIVER')
