from loguru import logger 
from core.parse_emails import email_parser, retrain

def get_filter_email_data():
    retrain()

    email_data = email_parser()    
    # logger.info(email_data)
    print(email_data)

if __name__ == "__main__":
    get_filter_email_data()
