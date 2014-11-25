from flask import Flask
from flask import make_response
import json
app = Flask(__name__)
app.config.from_envvar('CONFIG_FILE')

@app.route('/')
def index():
    return make_response(open('static/index.html').read())


@app.route('/get_classes', methods=['GET'])
def get_classes():
    return make_response(res)


if __name__ == '__main__':
    app.run()

