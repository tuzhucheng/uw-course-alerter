import os

import sendgrid

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
    sg = sendgrid.SendGridClient(os.environ['SENDGRID_USERNAME'], os.environ['SENDGRID_PASSWORD'])

    message = sendgrid.Mail()
    message.add_to(recipient)
    message.set_subject('UW Course Alerter: Classes Open')
    message.set_html(text)
    message.set_from('UW Course Alerter')
    status, msg = sg.send(message)
