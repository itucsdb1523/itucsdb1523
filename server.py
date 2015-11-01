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

#import classes for recurve_sportsmen table
from recurve_sportsmen import Recurver
from recurveCol import recurveCollection
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

        #create users table
        query = """ DROP TABLE IF EXISTS USERS """
        cursor.execute(query)

        query = """CREATE TABLE users (
            id serial PRIMARY KEY,
            email character varying(50) NOT NULL,
            password character varying(20) NOT NULL,
            username character varying(25) NOT NULL,
            secret_question character varying(50),
            secret_answer character varying(50)
            )"""
        cursor.execute(query)

        #create countries table
        query = """ DROP TABLE IF EXISTS COUNTRIES """
        cursor.execute(query)

        query = """CREATE TABLE countries (
            id serial PRIMARY KEY,
            country_code character varying(2) NOT NULL,
            name character varying(64) NOT NULL
            )"""
        cursor.execute(query)

        #insert countries
        query = """
        INSERT INTO countries VALUES (1, 'AF', 'Afghanistan');
        INSERT INTO countries VALUES (2, 'AL', 'Albania');
        INSERT INTO countries VALUES (3, 'DZ', 'Algeria');
        INSERT INTO countries VALUES (4, 'AS', 'American Samoa');
        INSERT INTO countries VALUES (5, 'AD', 'Andorra');
        INSERT INTO countries VALUES (6, 'AO', 'Angola');
        INSERT INTO countries VALUES (7, 'AI', 'Anguilla');
        INSERT INTO countries VALUES (8, 'AQ', 'Antarctica');
        INSERT INTO countries VALUES (9, 'AG', 'Antigua and Barbuda');
        INSERT INTO countries VALUES (10, 'AR', 'Argentina');
        INSERT INTO countries VALUES (11, 'AM', 'Armenia');
        INSERT INTO countries VALUES (12, 'AW', 'Aruba');
        INSERT INTO countries VALUES (13, 'AU', 'Australia');
        INSERT INTO countries VALUES (14, 'AT', 'Austria');
        INSERT INTO countries VALUES (15, 'AZ', 'Azerbaijan');
        INSERT INTO countries VALUES (16, 'BS', 'Bahamas');
        INSERT INTO countries VALUES (17, 'BH', 'Bahrain');
        INSERT INTO countries VALUES (18, 'BD', 'Bangladesh');
        INSERT INTO countries VALUES (19, 'BB', 'Barbados');
        INSERT INTO countries VALUES (20, 'BY', 'Belarus');
        INSERT INTO countries VALUES (21, 'BE', 'Belgium');
        INSERT INTO countries VALUES (22, 'BZ', 'Belize');
        INSERT INTO countries VALUES (23, 'BJ', 'Benin');
        INSERT INTO countries VALUES (24, 'BM', 'Bermuda');
        INSERT INTO countries VALUES (25, 'BT', 'Bhutan');
        INSERT INTO countries VALUES (26, 'BO', 'Bolivia');
        INSERT INTO countries VALUES (27, 'BA', 'Bosnia and Herzegovina');
        INSERT INTO countries VALUES (28, 'BW', 'Botswana');
        INSERT INTO countries VALUES (29, 'BV', 'Bouvet Island');
        INSERT INTO countries VALUES (30, 'BR', 'Brazil');
        INSERT INTO countries VALUES (31, 'BQ', 'British Antarctic Territory');
        INSERT INTO countries VALUES (32, 'IO', 'British Indian Ocean Territory');
        INSERT INTO countries VALUES (33, 'VG', 'British Virgin Islands');
        INSERT INTO countries VALUES (34, 'BN', 'Brunei');
        INSERT INTO countries VALUES (35, 'BG', 'Bulgaria');
        INSERT INTO countries VALUES (36, 'BF', 'Burkina Faso');
        INSERT INTO countries VALUES (37, 'BI', 'Burundi');
        INSERT INTO countries VALUES (38, 'KH', 'Cambodia');
        INSERT INTO countries VALUES (39, 'CM', 'Cameroon');
        INSERT INTO countries VALUES (40, 'CA', 'Canada');
        INSERT INTO countries VALUES (41, 'CT', 'Canton and Enderbury Islands');
        INSERT INTO countries VALUES (42, 'CV', 'Cape Verde');
        INSERT INTO countries VALUES (43, 'KY', 'Cayman Islands');
        INSERT INTO countries VALUES (44, 'CF', 'Central African Republic');
        INSERT INTO countries VALUES (45, 'TD', 'Chad');
        INSERT INTO countries VALUES (46, 'CL', 'Chile');
        INSERT INTO countries VALUES (47, 'CN', 'China');
        INSERT INTO countries VALUES (48, 'CX', 'Christmas Island');
        INSERT INTO countries VALUES (49, 'CC', 'Cocos [Keeling] Islands');
        INSERT INTO countries VALUES (50, 'CO', 'Colombia');
        INSERT INTO countries VALUES (51, 'KM', 'Comoros');
        INSERT INTO countries VALUES (52, 'CG', 'Congo - Brazzaville');
        INSERT INTO countries VALUES (53, 'CD', 'Congo - Kinshasa');
        INSERT INTO countries VALUES (54, 'CK', 'Cook Islands');
        INSERT INTO countries VALUES (55, 'CR', 'Costa Rica');
        INSERT INTO countries VALUES (56, 'HR', 'Croatia');
        INSERT INTO countries VALUES (57, 'CU', 'Cuba');
        INSERT INTO countries VALUES (58, 'CY', 'Cyprus');
        INSERT INTO countries VALUES (59, 'CZ', 'Czech Republic');
        INSERT INTO countries VALUES (60, 'CI', 'Cote dIvoire');
        INSERT INTO countries VALUES (61, 'DK', 'Denmark');
        INSERT INTO countries VALUES (62, 'DJ', 'Djibouti');
        INSERT INTO countries VALUES (63, 'DM', 'Dominica');
        INSERT INTO countries VALUES (64, 'DO', 'Dominican Republic');
        INSERT INTO countries VALUES (65, 'NQ', 'Dronning Maud Land');
        INSERT INTO countries VALUES (66, 'DD', 'East Germany');
        INSERT INTO countries VALUES (67, 'EC', 'Ecuador');
        INSERT INTO countries VALUES (68, 'EG', 'Egypt');
        INSERT INTO countries VALUES (69, 'SV', 'El Salvador');
        INSERT INTO countries VALUES (70, 'GQ', 'Equatorial Guinea');
        INSERT INTO countries VALUES (71, 'ER', 'Eritrea');
        INSERT INTO countries VALUES (72, 'EE', 'Estonia');
        INSERT INTO countries VALUES (73, 'ET', 'Ethiopia');
        INSERT INTO countries VALUES (74, 'FK', 'Falkland Islands');
        INSERT INTO countries VALUES (75, 'FO', 'Faroe Islands');
        INSERT INTO countries VALUES (76, 'FJ', 'Fiji');
        INSERT INTO countries VALUES (77, 'FI', 'Finland');
        INSERT INTO countries VALUES (78, 'FR', 'France');
        INSERT INTO countries VALUES (79, 'GF', 'French Guiana');
        INSERT INTO countries VALUES (80, 'PF', 'French Polynesia');
        INSERT INTO countries VALUES (81, 'TF', 'French Southern Territories');
        INSERT INTO countries VALUES (82, 'FQ', 'French Southern and Antarctic Territories');
        INSERT INTO countries VALUES (83, 'GA', 'Gabon');
        INSERT INTO countries VALUES (84, 'GM', 'Gambia');
        INSERT INTO countries VALUES (85, 'GE', 'Georgia');
        INSERT INTO countries VALUES (86, 'DE', 'Germany');
        INSERT INTO countries VALUES (87, 'GH', 'Ghana');
        INSERT INTO countries VALUES (88, 'GI', 'Gibraltar');
        INSERT INTO countries VALUES (89, 'GR', 'Greece');
        INSERT INTO countries VALUES (90, 'GL', 'Greenland');
        INSERT INTO countries VALUES (91, 'GD', 'Grenada');
        INSERT INTO countries VALUES (92, 'GP', 'Guadeloupe');
        INSERT INTO countries VALUES (93, 'GU', 'Guam');
        INSERT INTO countries VALUES (94, 'GT', 'Guatemala');
        INSERT INTO countries VALUES (95, 'GG', 'Guernsey');
        INSERT INTO countries VALUES (96, 'GN', 'Guinea');
        INSERT INTO countries VALUES (97, 'GW', 'Guinea-Bissau');
        INSERT INTO countries VALUES (98, 'GY', 'Guyana');
        INSERT INTO countries VALUES (99, 'HT', 'Haiti');
        INSERT INTO countries VALUES (100, 'HM', 'Heard Island and McDonald Islands');
        INSERT INTO countries VALUES (101, 'HN', 'Honduras');
        INSERT INTO countries VALUES (102, 'HK', 'Hong Kong SAR China');
        INSERT INTO countries VALUES (103, 'HU', 'Hungary');
        INSERT INTO countries VALUES (104, 'IS', 'Iceland');
        INSERT INTO countries VALUES (105, 'IN', 'India');
        INSERT INTO countries VALUES (106, 'ID', 'Indonesia');
        INSERT INTO countries VALUES (107, 'IR', 'Iran');
        INSERT INTO countries VALUES (108, 'IQ', 'Iraq');
        INSERT INTO countries VALUES (109, 'IE', 'Ireland');
        INSERT INTO countries VALUES (110, 'IM', 'Isle of Man');
        INSERT INTO countries VALUES (111, 'IL', 'Israel');
        INSERT INTO countries VALUES (112, 'IT', 'Italy');
        INSERT INTO countries VALUES (113, 'JM', 'Jamaica');
        INSERT INTO countries VALUES (114, 'JP', 'Japan');
        INSERT INTO countries VALUES (115, 'JE', 'Jersey');
        INSERT INTO countries VALUES (116, 'JT', 'Johnston Island');
        INSERT INTO countries VALUES (117, 'JO', 'Jordan');
        INSERT INTO countries VALUES (118, 'KZ', 'Kazakhstan');
        INSERT INTO countries VALUES (119, 'KE', 'Kenya');
        INSERT INTO countries VALUES (120, 'KI', 'Kiribati');
        INSERT INTO countries VALUES (121, 'KW', 'Kuwait');
        INSERT INTO countries VALUES (122, 'KG', 'Kyrgyzstan');
        INSERT INTO countries VALUES (123, 'LA', 'Laos');
        INSERT INTO countries VALUES (124, 'LV', 'Latvia');
        INSERT INTO countries VALUES (125, 'LB', 'Lebanon');
        INSERT INTO countries VALUES (126, 'LS', 'Lesotho');
        INSERT INTO countries VALUES (127, 'LR', 'Liberia');
        INSERT INTO countries VALUES (128, 'LY', 'Libya');
        INSERT INTO countries VALUES (129, 'LI', 'Liechtenstein');
        INSERT INTO countries VALUES (130, 'LT', 'Lithuania');
        INSERT INTO countries VALUES (131, 'LU', 'Luxembourg');
        INSERT INTO countries VALUES (132, 'MO', 'Macau SAR China');
        INSERT INTO countries VALUES (133, 'MK', 'Macedonia');
        INSERT INTO countries VALUES (134, 'MG', 'Madagascar');
        INSERT INTO countries VALUES (135, 'MW', 'Malawi');
        INSERT INTO countries VALUES (136, 'MY', 'Malaysia');
        INSERT INTO countries VALUES (137, 'MV', 'Maldives');
        INSERT INTO countries VALUES (138, 'ML', 'Mali');
        INSERT INTO countries VALUES (139, 'MT', 'Malta');
        INSERT INTO countries VALUES (140, 'MH', 'Marshall Islands');
        INSERT INTO countries VALUES (141, 'MQ', 'Martinique');
        INSERT INTO countries VALUES (142, 'MR', 'Mauritania');
        INSERT INTO countries VALUES (143, 'MU', 'Mauritius');
        INSERT INTO countries VALUES (144, 'YT', 'Mayotte');
        INSERT INTO countries VALUES (145, 'FX', 'Metropolitan France');
        INSERT INTO countries VALUES (146, 'MX', 'Mexico');
        INSERT INTO countries VALUES (147, 'FM', 'Micronesia');
        INSERT INTO countries VALUES (148, 'MI', 'Midway Islands');
        INSERT INTO countries VALUES (149, 'MD', 'Moldova');
        INSERT INTO countries VALUES (150, 'MC', 'Monaco');
        INSERT INTO countries VALUES (151, 'MN', 'Mongolia');
        INSERT INTO countries VALUES (152, 'ME', 'Montenegro');
        INSERT INTO countries VALUES (153, 'MS', 'Montserrat');
        INSERT INTO countries VALUES (154, 'MA', 'Morocco');
        INSERT INTO countries VALUES (155, 'MZ', 'Mozambique');
        INSERT INTO countries VALUES (156, 'MM', 'Myanmar [Burma]');
        INSERT INTO countries VALUES (157, 'NA', 'Namibia');
        INSERT INTO countries VALUES (158, 'NR', 'Nauru');
        INSERT INTO countries VALUES (159, 'NP', 'Nepal');
        INSERT INTO countries VALUES (160, 'NL', 'Netherlands');
        INSERT INTO countries VALUES (161, 'AN', 'Netherlands Antilles');
        INSERT INTO countries VALUES (162, 'NT', 'Neutral Zone');
        INSERT INTO countries VALUES (163, 'NC', 'New Caledonia');
        INSERT INTO countries VALUES (164, 'NZ', 'New Zealand');
        INSERT INTO countries VALUES (165, 'NI', 'Nicaragua');
        INSERT INTO countries VALUES (166, 'NE', 'Niger');
        INSERT INTO countries VALUES (167, 'NG', 'Nigeria');
        INSERT INTO countries VALUES (168, 'NU', 'Niue');
        INSERT INTO countries VALUES (169, 'NF', 'Norfolk Island');
        INSERT INTO countries VALUES (170, 'KP', 'North Korea');
        INSERT INTO countries VALUES (171, 'VD', 'North Vietnam');
        INSERT INTO countries VALUES (172, 'MP', 'Northern Mariana Islands');
        INSERT INTO countries VALUES (173, 'NO', 'Norway');
        INSERT INTO countries VALUES (174, 'OM', 'Oman');
        INSERT INTO countries VALUES (175, 'PC', 'Pacific Islands Trust Territory');
        INSERT INTO countries VALUES (176, 'PK', 'Pakistan');
        INSERT INTO countries VALUES (177, 'PW', 'Palau');
        INSERT INTO countries VALUES (178, 'PS', 'Palestinian Territories');
        INSERT INTO countries VALUES (179, 'PA', 'Panama');
        INSERT INTO countries VALUES (180, 'PZ', 'Panama Canal Zone');
        INSERT INTO countries VALUES (181, 'PG', 'Papua New Guinea');
        INSERT INTO countries VALUES (182, 'PY', 'Paraguay');
        INSERT INTO countries VALUES (183, 'PE', 'Peru');
        INSERT INTO countries VALUES (184, 'PH', 'Philippines');
        INSERT INTO countries VALUES (185, 'PN', 'Pitcairn Islands');
        INSERT INTO countries VALUES (186, 'PL', 'Poland');
        INSERT INTO countries VALUES (187, 'PT', 'Portugal');
        INSERT INTO countries VALUES (188, 'PR', 'Puerto Rico');
        INSERT INTO countries VALUES (189, 'QA', 'Qatar');
        INSERT INTO countries VALUES (190, 'RO', 'Romania');
        INSERT INTO countries VALUES (191, 'RU', 'Russia');
        INSERT INTO countries VALUES (192, 'RW', 'Rwanda');
        INSERT INTO countries VALUES (193, 'RE', 'Reunion');
        INSERT INTO countries VALUES (194, 'BL', 'Saint Barthelemy');
        INSERT INTO countries VALUES (195, 'SH', 'Saint Helena');
        INSERT INTO countries VALUES (196, 'KN', 'Saint Kitts and Nevis');
        INSERT INTO countries VALUES (197, 'LC', 'Saint Lucia');
        INSERT INTO countries VALUES (198, 'MF', 'Saint Martin');
        INSERT INTO countries VALUES (199, 'PM', 'Saint Pierre and Miquelon');
        INSERT INTO countries VALUES (200, 'VC', 'Saint Vincent and the Grenadines');
        INSERT INTO countries VALUES (201, 'WS', 'Samoa');
        INSERT INTO countries VALUES (202, 'SM', 'San Marino');
        INSERT INTO countries VALUES (203, 'SA', 'Saudi Arabia');
        INSERT INTO countries VALUES (204, 'SN', 'Senegal');
        INSERT INTO countries VALUES (205, 'RS', 'Serbia');
        INSERT INTO countries VALUES (206, 'CS', 'Serbia and Montenegro');
        INSERT INTO countries VALUES (207, 'SC', 'Seychelles');
        INSERT INTO countries VALUES (208, 'SL', 'Sierra Leone');
        INSERT INTO countries VALUES (209, 'SG', 'Singapore');
        INSERT INTO countries VALUES (210, 'SK', 'Slovakia');
        INSERT INTO countries VALUES (211, 'SI', 'Slovenia');
        INSERT INTO countries VALUES (212, 'SB', 'Solomon Islands');
        INSERT INTO countries VALUES (213, 'SO', 'Somalia');
        INSERT INTO countries VALUES (214, 'ZA', 'South Africa');
        INSERT INTO countries VALUES (215, 'GS', 'South Georgia and the South Sandwich Islands');
        INSERT INTO countries VALUES (216, 'KR', 'South Korea');
        INSERT INTO countries VALUES (217, 'ES', 'Spain');
        INSERT INTO countries VALUES (218, 'LK', 'Sri Lanka');
        INSERT INTO countries VALUES (219, 'SD', 'Sudan');
        INSERT INTO countries VALUES (220, 'SR', 'Suriname');
        INSERT INTO countries VALUES (221, 'SJ', 'Svalbard and Jan Mayen');
        INSERT INTO countries VALUES (222, 'SZ', 'Swaziland');
        INSERT INTO countries VALUES (223, 'SE', 'Sweden');
        INSERT INTO countries VALUES (224, 'CH', 'Switzerland');
        INSERT INTO countries VALUES (225, 'SY', 'Syria');
        INSERT INTO countries VALUES (226, 'ST', 'Sao Tome and Principe');
        INSERT INTO countries VALUES (227, 'TW', 'Taiwan');
        INSERT INTO countries VALUES (228, 'TJ', 'Tajikistan');
        INSERT INTO countries VALUES (229, 'TZ', 'Tanzania');
        INSERT INTO countries VALUES (230, 'TH', 'Thailand');
        INSERT INTO countries VALUES (231, 'TL', 'Timor-Leste');
        INSERT INTO countries VALUES (232, 'TG', 'Togo');
        INSERT INTO countries VALUES (233, 'TK', 'Tokelau');
        INSERT INTO countries VALUES (234, 'TO', 'Tonga');
        INSERT INTO countries VALUES (235, 'TT', 'Trinidad and Tobago');
        INSERT INTO countries VALUES (236, 'TN', 'Tunisia');
        INSERT INTO countries VALUES (237, 'TR', 'Turkey');
        INSERT INTO countries VALUES (238, 'TM', 'Turkmenistan');
        INSERT INTO countries VALUES (239, 'TC', 'Turks and Caicos Islands');
        INSERT INTO countries VALUES (240, 'TV', 'Tuvalu');
        INSERT INTO countries VALUES (241, 'UM', 'U.S. Minor Outlying Islands');
        INSERT INTO countries VALUES (242, 'PU', 'U.S. Miscellaneous Pacific Islands');
        INSERT INTO countries VALUES (243, 'VI', 'U.S. Virgin Islands');
        INSERT INTO countries VALUES (244, 'UG', 'Uganda');
        INSERT INTO countries VALUES (245, 'UA', 'Ukraine');
        INSERT INTO countries VALUES (246, 'SU', 'Union of Soviet Socialist Republics');
        INSERT INTO countries VALUES (247, 'AE', 'United Arab Emirates');
        INSERT INTO countries VALUES (248, 'GB', 'United Kingdom');
        INSERT INTO countries VALUES (249, 'US', 'United States');
        INSERT INTO countries VALUES (250, 'ZZ', 'Unknown or Invalid Region');
        INSERT INTO countries VALUES (251, 'UY', 'Uruguay');
        INSERT INTO countries VALUES (252, 'UZ', 'Uzbekistan');
        INSERT INTO countries VALUES (253, 'VU', 'Vanuatu');
        INSERT INTO countries VALUES (254, 'VA', 'Vatican City');
        INSERT INTO countries VALUES (255, 'VE', 'Venezuela');
        INSERT INTO countries VALUES (256, 'VN', 'Vietnam');
        INSERT INTO countries VALUES (257, 'WK', 'Wake Island');
        INSERT INTO countries VALUES (258, 'WF', 'Wallis and Futuna');
        INSERT INTO countries VALUES (259, 'EH', 'Western Sahara');
        INSERT INTO countries VALUES (260, 'YE', 'Yemen');
        INSERT INTO countries VALUES (261, 'ZM', 'Zambia');
        INSERT INTO countries VALUES (262, 'ZW', 'Zimbabwe');
        INSERT INTO countries VALUES (263, 'AX', 'Aland Islands');"""
        cursor.execute(query)

        #create recursive_sportsmen table
        query = """ DROP TABLE IF EXISTS RECURVE_SPORTSMEN """
        cursor.execute(query)

        query = """
        CREATE TABLE recurve_sportsmen (
        id serial PRIMARY KEY,
        name character varying(20) NOT NULL,
        surname character varying(30) NOT NULL,
        birth_year integer,
        country_id integer NOT NULL references countries(id)
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

@app.route('/recurve_archery', methods=['GET', 'POST'])
def recurve_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor=connection.cursor()
    Message=""
    #display recurvers
    if request.method == 'GET':
        statement="""SELECT * FROM countries"""
        cursor.execute(statement)
        countries=cursor.fetchall()
        now = datetime.datetime.now()
        thisYear=datetime.datetime.today().year
        statement="""SELECT * FROM recurve_sportsmen"""
        cursor.execute(statement)
        allRecurvers=recurveCollection()
        for row in cursor:
            id, name, surname, birth_year, country_id = row
            allRecurvers.add_recurver(Recurver(id, name, surname, birth_year, country_id))
        cursor.close()
        return render_template('recurve.html', recurvers=allRecurvers.get_recurvers(), allCountries=countries, current_time=now.ctime(), rec_Message=Message, current_year=thisYear)

    #delete from recurve sportsmen
    elif 'recurvers_to_delete' in request.form:
        keys = request.form.getlist('recurvers_to_delete')
        for key in keys:
            statement="""DELETE FROM recurve_sportsmen WHERE ("ID"=%s)"""
            cursor.execute(statement, (key,))
        connection.commit()
        cursor.close()
        return redirect(url_for('recurve_page'))


    #insert to recurve sportsmen
    else:
        new_name=request.form['name']
        new_surname=request.form['surname']
        new_age=request.form['age']
        new_country_id=request.form['country_id']
        new_birth_year=datetime.datetime.today().year-int(float(new_age))
        Message="Insertion successfull!"
        try:
            statement="""SELECT * FROM recurve_sportsmen WHERE (NAME=%s) AND (SURNAME=%s)"""
            cursor.execute(statement, (new_name, new_surname))
            recurver=cursor.fetchone()
            if recurver is not None:
                Message="Sorry, this recurve sportsman already exists."
                cursor.close()
                connection.close()
                return redirect(url_for('recurve_page'))
            else: #try to insert
                statement="""INSERT INTO recurve_sportsmen (name, surname, birth_year, country_id) VALUES(%s, %s, %s, %s)"""
                cursor.execute(statement, (new_name, new_surname, new_birth_year, new_country_id))
                connection.commit()
        except dbapi2.DatabaseError:
            connection.rollback()
            Message="Registration failed due to a Database Error."
    cursor.close()
    connection.close()
    return redirect(url_for('recurve_page'))

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    now = datetime.datetime.now()
    anyError=0
    if request.method == 'GET':
        return render_template('register.html', current_time=now.ctime())
    else:
        try:
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor=connection.cursor()
            inputUsername=request.form['username']
            statement="""SELECT * FROM Users WHERE (USERNAME=%s)"""
            cursor.execute(statement, (inputUsername,))
            users=cursor.fetchone()
            if users is not None:
                registerMessage="Sorry, this username is already taken."
                anyError=1
                return
            inputEmail=request.form['email']
            statement="""SELECT * FROM Users WHERE (EMAIL=%s)"""
            cursor.execute(statement, (inputEmail,))
            users=cursor.fetchone()
            if users is not None:
                registerMessage="This email address is already registered."
                anyError=1
                return
            inputPassword= request.form['password']
            secretQuestion= request.form['sec_question']
            secretAnswer= request.form['sec_answer']
            statement="""INSERT INTO Users (username, email, password, secret_question, secret_answer) VALUES(%s, %s, %s, %s, %s)"""
            cursor.execute(statement, (inputUsername, inputEmail, inputPassword, secretQuestion, secretAnswer))
            connection.commit()
            cursor.close()
        except dbapi2.DatabaseError:
            connection.rollback()
            registerMessage="Registration failed due to a Database Error."
            anyError=1
        finally:
            connection.close()
            if anyError==1:
                return render_template('register.html', current_time=now.ctime(), message=registerMessage)
            else:
                registerMessage="Registration was successfull. Please, sign in above."
                return render_template('sign_in.html', current_time=now.ctime(), message=registerMessage)

@app.route('/sign_in',methods=['GET', 'POST'])
def sign_in_page():
    now = datetime.datetime.now()
    if request.method == 'GET':
        return render_template('sign_in.html', current_time=now.ctime(), message="")
    else:
        try:
            with dbapi2.connect(app.config['dsn']) as connection:
                cursor=connection.cursor()
            inputEmail=request.form['email']
            inputPassword=request.form['password']
            statement="""SELECT * FROM Users WHERE (EMAIL=%s) AND (PASSWORD=%s)"""
            cursor.execute(statement, (inputEmail, inputPassword))
            users=cursor.fetchall()
        except dbapi2.DatabaseError:
            connection.rollback()
        finally:
            cursor.close()
            connection.close()
        if len(users)==0:
            return render_template('sign_in.html', current_time=now.ctime(), message="Wrong email or password!")
        else:
            return render_template('home.html', current_time=now.ctime())


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
