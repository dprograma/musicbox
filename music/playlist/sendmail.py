from email import message
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

MAIL_PORT = config('MAIL_PORT')
MAIL_SERVER = config('MAIL_SERVER')
MAIL_USER = config('MAIL_USER')
MAIL_PASS = config('MAIL_PASS')

class SendMail:
    def __init__(self, to, subject, message, altmsg):
        self.to = to
        self.subject = subject
        self.message = message
        self.altmsg = altmsg
        self.send()
        print("Email sent successfully")

    def send(self):
        port = MAIL_PORT # For starttls
        smtp_server = MAIL_SERVER
        sender_email = MAIL_USER
        password = MAIL_PASS
        receiver_email = self.to

        message = MIMEMultipart("alternative")
        message["Subject"] = self.subject
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = self.altmsg
        html = self.message

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())