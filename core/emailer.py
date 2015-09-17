import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template


def generate_open_sections_email(subject, cournum, sections):
    template = Template("""
    <h1>There are sections open for {{ subject }} {{ cournum }}!</h1>
    <ul>
        {% for section in sections if section['enroll_total'] < section['enroll_cap'] %}
        <li>{{ section['component'] }} {{ section['section'] }} taught by {{ section['prof'] }} at {{ section['room'] }} from {{ section['time'] }} has {{ section['enroll_total'] }} out of {{ section['enroll_cap'] }} students enrolled.</li>
        {% endfor %}
    </ul>
    """)
    return template.render(subject=subject, cournum=cournum, sections=sections)


def send_html_mail(recipient, text):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "UW Course Alerter"
    msg['From']    = "UW Course Alerter <uw-alerter@heroku.com>" # Your from name and email address
    msg['To']      = recipient

    username = os.environ['MANDRILL_USERNAME']
    password = os.environ['MANDRILL_APIKEY']
    body = MIMEText(text, 'html', 'utf-8')
    msg.attach(body)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)
    try:
        s.login(username, password)
        s.sendmail(msg['From'], msg['To'], msg.as_string())
    except smtplib.SMTPAuthenticationError as e:
        print 'SMTP Authentication Error! {}'.format(e)

    s.quit()

