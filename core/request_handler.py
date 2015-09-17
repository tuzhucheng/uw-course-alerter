import urllib, urllib2
import json
import re

from flask import Response
from flask import make_response, request

from request_helper import validate_fields_exist, make_error_response
import scraper
import emailer
import authorization


def check_availability():
    validate_state, validate_res = validate_fields_exist(['level', 'session', 'subject', 'number', 'email'])
    if not validate_state:
        return validate_res

    level = request.form['level']
    sess = int(request.form['session'])
    subject = request.form['subject']
    cournum = request.form['number']
    email_address = request.form['email']
    sec = request.form.get('sec')

    email_pattern = r'[^@]+@[^@]+\.[^@]+'
    if not re.match(email_pattern, email_address):
        return make_error_response('{} is not a valid email address'.format(email_address))

    auth_status = authorization.authorize(email_address)
    if not auth_status:
        return make_error_response('{} is not added to the whitelist, please contact the developer.'.format(email_address), 401)

    url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
    values = {'level': level, 'sess': sess, 'subject': subject, 'cournum': cournum}
    data = urllib.urlencode(values)

    req = urllib2.Request(url, data)
    try:
        res = urllib2.urlopen(req)
    except urllib2.HTTPError as e:
        return make_error_response('HTTP Error: {}'.format(e))
    except urllib2.URLError as e:
        return make_error_response('URL Error: {}'.format(e))

    page = res.read()
    blocks = scraper.extract_blocks(page)
    blocks_str = json.dumps(blocks)
    blocks_str += '\n'

    should_alert = False
    for block in blocks:
        if block['enroll_total'] < block['enroll_cap']:
            if not sec or sec == block['section']:
                should_alert = True
                break

    if should_alert:
        email_str = emailer.generate_open_sections_email(subject, cournum, blocks)
        emailer.send_html_mail(email_address, email_str)

    api_res = Response(blocks_str, 200, mimetype='application/json')
    return make_response(api_res)

