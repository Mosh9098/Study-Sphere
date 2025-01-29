import sendgrid
from sendgrid.helpers.mail import Mail
from flask import current_app

def send_email(to_email, subject, content):
    sg = sendgrid.SendGridAPIClient(api_key=current_app.config['SENDGRID_API_KEY'])
    message = Mail(
        from_email=current_app.config['DEFAULT_FROM_EMAIL'],
        to_emails=to_email,
        subject=subject,
        html_content=content
    )
    try:
        sg.send(message)
    except Exception as e:
        print(str(e))
