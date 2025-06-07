import base64
from config.gmail_auth import get_token
from googleapiclient.discovery import build
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dashboard.report_generator import generate_report

FROM_EMAIL = 'mkolhe23@gmail.com'
SUBJECT = 'Daily Transcations Summary Report'

def generate_alert(to_mail, message_text):
    creds = get_token()
    token =  build('gmail', 'v1', credentials=creds)
    message = MIMEMultipart()
    message['to'] = to_mail
    message['from'] = FROM_EMAIL
    message['subject'] = SUBJECT
    message.attach(MIMEText(message_text, 'html'))
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    sent_message = token.users().messages().send(userId="me", body={'raw': raw}).execute()
    print(f"Email sent! Message ID: {sent_message['id']}")


def send_email_alert():
    to_mail = FROM_EMAIL
    report = generate_report()
    html_report = report.to_html(index=False,border=0,classes='table',justify='center')

    html_content = f"""
                    <html>
                        <head>
                            <style>
                                table {{
                                    width: 60%;
                                    border-collapse: collapse;
                                    margin: 20px auto;
                                    font-family: Arial, sans-serif;
                                }}
                                th, td {{
                                    border: 1px solid #dddddd;
                                    text-align: center;
                                    padding: 8px;
                                }}
                                th {{
                                    background-color: #4CAF50;
                                    color: white;
                                }}
                                tr:nth-child(even) {{
                                    background-color: #f2f2f2;
                                }}
                            </style>
                        </head>
                        <body>
                            <h2 style="text-align:center;">📊 Daily Expense Report</h2>
                            {html_report}
                        </body>
                    </html>
                    """
    generate_alert(to_mail, html_content)
