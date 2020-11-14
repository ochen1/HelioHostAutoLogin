import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# For Gmail accounts, make sure to turn on less secure apps access using the link below:
# https://myaccount.google.com/u/1/lesssecureapps


def gen_message(sender_email, receiver_email, subject, text, html=None):
    """Generate a message to be sent in an email."""
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(text, "plain"))
    if html:
        message.attach(MIMEText(html, "html"))

    return message


def send_email(sender_email, receiver_email, password, message):
    """Send an email."""
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email,
            receiver_email,
            message.as_string()
        )
