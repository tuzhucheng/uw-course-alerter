import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


def send_plain_text_mail(recipient, text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "UW Course Alerter"
    msg['From']    = "UW Course Alerter <uw-alerter@heroku.com>" # Your from name and email address
    msg['To']      = recipient

    username = os.environ['MANDRILL_USERNAME']
    password = os.environ['MANDRILL_APIKEY']
    body = MIMEText(text, 'plain')
    msg.attach(body)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)
    try:
        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    except smtplib.SMTPAuthenticationError as e:
        print 'SMTP Authentication Error! {}'.format(e)

    s.quit()

