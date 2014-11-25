from flask import Flask
from flask import make_response
import urllib, urllib2
app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')

@app.route('/')
def index():
    return make_response(open('static/index.html').read())


@app.route('/get_classes', methods=['GET'])
def get_classes():
    # TODO: replace hardcoded, static data with query in GET request
    level = 'under'
    sess = 1151
    subject = 'CS'
    cournum = 341
    url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
    values = {'level': level, 'sess': sess, 'subject': subject, 'cournum': cournum}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    res = urllib2.urlopen(req)
    page = res.read()
    return make_response(page)


if __name__ == '__main__':
    app.run()

