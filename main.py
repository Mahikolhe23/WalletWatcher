from loguru import logger 
from core.filter_email import filter_email

def get_filter_email_data():
    email_data = filter_email()    
    logger.info(email_data)

if __name__ == "__main__":
    get_filter_email_data()
