from loguru import logger 
from core.parse_emails import retrain
from data.save_trans import save_trans_to_db 
from dashboard.report_generator import generate_report
from services.email_notifier import send_email_alert
from core.parse_emails import email_parser
from services.password_remover import remove_password

def get_filter_email_data():
    file_path = '/Users/mahendrakolhe/Projects/WalletWatcher/data/downloaded_files'
    # Train Model
    retrain()

    # Save Parse data to db
    # save_trans_to_db(file_path)
    
    user_name = 'Mahendra'
    email_parser(file_path, user_name)
    remove_password(file_path)
    
    # Generate report
    # report = generate_report()
    # print(report)

    # send_email_alert()


if __name__ == "__main__":
    get_filter_email_data()
