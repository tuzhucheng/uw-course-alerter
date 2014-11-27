from flask import Response
from flask import make_response, request
import urllib, urllib2
import json

from request_helper import validate_fields_exist, make_error_response
import scraper
import emailer


def check_availability():
    validate_state, validate_res = validate_fields_exist(['level', 'session', 'subject', 'number', 'email'])
    if not validate_state:
        return validate_res

    level = request.form['level']
    sess = int(request.form['session'])
    subject = request.form['subject']
    cournum = int(request.form['number'])
    email_address = request.form['email']

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
    sections = scraper.extract_sections(page)
    sections_str = json.dumps(sections)

    emailer.send_plain_text_mail(email_address, sections_str)

    api_res = Response(sections_str, 200, mimetype='application/json')
    return make_response(api_res)

