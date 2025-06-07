from loguru import logger 
from core.parse_emails import retrain
from data.save_trans import save_trans_to_db 
from dashboard.report_generator import generate_report

def get_filter_email_data():
    # Train Model
    retrain()

    # Save Parse data to db
    save_trans_to_db()

    # Generate report
    report = generate_report()
    print(report)






if __name__ == "__main__":
    get_filter_email_data()
