import datetime
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())
@app.route('/recurve_archery')
def recurve_page():
    now = datetime.datetime.now()
    return render_template('recurve.html', current_time=now.ctime())

@app.route('/sign_in')
def sign_in_page():
    now = datetime.datetime.now()
    return render_template('sign_in.html', current_time=now.ctime())



if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    app.run(host='0.0.0.0', port=port, debug=debug)
