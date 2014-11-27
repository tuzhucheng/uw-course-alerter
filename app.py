from flask import Flask
from flask import make_response, request
import core.request_handler as request_handler

app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')

@app.route('/')
def index():
    return make_response(open('static/index.html').read())


@app.route('/check_availability', methods=['POST'])
def check_availability():
    return request_handler.check_availability()


if __name__ == '__main__':
    app.run()

