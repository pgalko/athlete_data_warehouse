import email, smtplib, ssl
import os.path
from database_ini_parser import config
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64

def send_email(encr_pass, subject, body, att_path=None, recipients=None):
    app_params = config(filename="encrypted_settings.ini", section="app",encr_pass=encr_pass)
    smtp_user = app_params.get("smtp_user")
    smtp_password = app_params.get("smtp_password")
    smtp_default_sender = app_params.get("smtp_default_sender")
    admin_email = app_params.get("admin_email")
    smtp_server = app_params.get("smtp_server")
    smtp_server_port = int(app_params.get("smtp_server_port"))

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = smtp_default_sender
    if recipients is not None:
        if isinstance(recipients, list):
            message["To"] = ", ".join(recipients)
        else:
            message["To"] = recipients
    else:
        recipients = admin_email
        message["To"] = recipients
    message["Subject"] = subject
    #message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    if att_path is not None:
        # Open attachement file in binary mode
        with open(att_path, "rb") as attachment:
            # Add file as application/octet-stream
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        filename = os.path.basename(os.path.normpath(att_path))

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename= %s" % filename
        )

        # Add attachment to message
        message.attach(part)
    # Convert message to string
    text = message.as_string()

    # Log in to server and send email
    server =  smtplib.SMTP_SSL(smtp_server, smtp_server_port)
    server.login(smtp_user, smtp_password)
    server.sendmail(smtp_default_sender, recipients, text)
