from flask import Flask
from flask import Response
from flask import make_response, request
from bs4 import BeautifulSoup
import urllib, urllib2
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')

@app.route('/')
def index():
    return make_response(open('static/index.html').read())


@app.route('/check_availability', methods=['POST'])
def check_availability():
    messages = []
    for required_field in ('level', 'session', 'subject', 'number', 'email'):
        if not required_field in request.form:
            messages.append(required_field)

    if len(messages):
        res_body = 'The following fields are missing:\n'
        for m in messages:
            res_body += m + '\n'
        res = Response(res_body, 400, mimetype='text/plain')
        return make_response(res)

    level = request.form['level']
    sess = int(request.form['session'])
    subject = request.form['subject']
    cournum = int(request.form['number'])
    email_address = request.form['email']

    url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
    values = {'level': level, 'sess': sess, 'subject': subject, 'cournum': cournum}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    res = urllib2.urlopen(req)
    page = res.read()

    soup = BeautifulSoup(page)
    table_rows = soup.find_all('tr')
    sections = []
    for row in table_rows[4:-2]:
        table_cells = row.find_all('td')
        if 'LEC' in table_cells[1].get_text():
            section = {'section': table_cells[1].get_text(),
                       'enroll_cap': table_cells[6].get_text(),
                       'enroll_total': table_cells[7].get_text(),
                       'time': table_cells[10].get_text(),
                       'room': table_cells[11].get_text(),
                       'prof': table_cells[12].get_text()}
            sections.append(section)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "UW Course Alerter"
    msg['From']    = "UW Course Alerter <uwcoursealerter@heroku.com>" # Your from name and email address
    msg['To']      = email_address

    username = os.environ['MANDRILL_USERNAME']
    password = os.environ['MANDRILL_APIKEY']
    body = MIMEText('This is a test email', 'plain')
    msg.attach(body)

    s = smtplib.SMTP('smtp.mandrillapp.com', 587)
    s.login(username, password)
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    api_res = Response(json.dumps(sections), 200, mimetype='application/json')
    return make_response(api_res)


if __name__ == '__main__':
    app.run()

