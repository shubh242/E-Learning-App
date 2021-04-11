# Using : https://docs.python.org/3/library/smtplib.html,
# https://docs.python.org/3/library/email.compat32-message.html?highlight=attach#email.message.Message.attach

import smtplib

#Imports for the File Parsing ( Using email.MIME ):
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

def send_email(email, otp):
    host = "smtp.gmail.com"
    port = 587
    username = '#'
    password = "#"  
    recipients = [email]

    # Adding and parsing an HTML File within the mail itself.
    # Letting know of possible HTML file
    the_msg = MIMEMultipart("alternative")
    the_msg['Subject'] = "OTP For Registration"
    the_msg['From'] = username
    the_msg['To'] = email
    plain_txt = str(otp)
    part_1 = MIMEText(plain_txt, 'plain')
    the_msg.attach(part_1)

    #Send Mail:
    email_conn = smtplib.SMTP(host, port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(username, password)
    email_conn.sendmail(username, recipients, the_msg.as_string())
    email_conn.quit()
