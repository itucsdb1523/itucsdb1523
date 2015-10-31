import datetime
import json
import os
import re
import psycopg2 as dbapi2

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask.helpers import url_for

#import classes for score table
from score import Score
from scoreCol import ScoreCol

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


@app.route('/', methods=['GET', 'POST'])
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdb')
def initialize_database():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        #initialize counter table
        query = """DROP TABLE IF EXISTS COUNTER"""
        cursor.execute(query)

        query = """CREATE TABLE COUNTER (N INTEGER)"""
        cursor.execute(query)

        query = """INSERT INTO COUNTER (N) VALUES (0)"""
        cursor.execute(query)

        #initialize score table (empty)
        query = """DROP TABLE IF EXISTS SCORE"""
        cursor.execute(query)

        query = """CREATE TABLE SCORE (
            ID SERIAL PRIMARY KEY,
            ARCHERID INTEGER,
            TOURNAMENTID INTEGER,
            SCORE INTEGER,
            UNIQUE (ARCHERID, TOURNAMENTID)
        )"""
        cursor.execute(query)

        connection.commit()
    return redirect(url_for('home_page'))

@app.route('/count')
def counter_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        query = """UPDATE COUNTER SET N = N + 1"""
        cursor.execute(query)
        connection.commit()

        query = """SELECT N FROM COUNTER"""
        cursor.execute(query)
        count = cursor.fetchone()[0]
    return 'This page was accessed %d times' % count

@app.route('/archery_scores', methods=['GET', 'POST'])
def scores_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor = connection.cursor()

        #display score table
        if request.method == 'GET':
            query = """SELECT ID, ARCHERID, TOURNAMENTID, SCORE FROM SCORE"""
            cursor.execute(query)
            s = ScoreCol()
            for row in cursor:
                id, archer_id, tournament_id, score = row
                s.add_score(Score(id, archer_id,tournament_id,score))
            scores = s.get_scores()

            now = datetime.datetime.now()
            return render_template('scores.html', current_time=now.ctime(), scores=scores)

        #delete from score table
        elif 'scores_to_delete' in request.form:
            keys = request.form.getlist('scores_to_delete')
            for key in keys:
                query = """DELETE FROM SCORE WHERE (ID = %s)"""
                cursor.execute(query,(key))

            connection.commit()

            return redirect(url_for('scores_page'))

        #add to the score table
        else:
            archer_id = request.form['archer_id']
            tournament_id = request.form['tournament_id']
            score = request.form['score']

            query = """INSERT INTO SCORE (ARCHERID, TOURNAMENTID, SCORE) VALUES (%s,%s,%s)"""
            cursor.execute(query,(archer_id,tournament_id,score))

            connection.commit()

            return redirect(url_for('scores_page'))

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

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=54321 dbname='itucsdb'"""

    app.run(host='0.0.0.0', port=port, debug=debug)
