Parts Implemented by Muhammet Afşin Karataş
===========================================

Mounted Sportsmen Table
-----------------------

Creating
^^^^^^^^

Below is the MOUNTED_SPORTSMEN table;

+-----------------+-----------------------+--------------+
| Name            | Type                  | Restrictions |
+=================+=======================+==============+
| ID              | integer               | Primary key  |
+-----------------+-----------------------+--------------+
| NAME            | character varying(20) | Not null     |
+-----------------+-----------------------+--------------+
| SURNAME         | character varying(30) | Not null     |
+-----------------+-----------------------+--------------+
| BIRTH_YEAR      | integer               |              |
+-----------------+-----------------------+--------------+
| COUNTRY_ID      | integer               | Foreign key, |
|                 |                       | Not null     |
+-----------------+-----------------------+--------------+

COUNTRY_ID references to countries table

.. code-block:: sql

      query = """ DROP TABLE IF EXISTS MOUNTED_SPORTSMEN """
      cursor.execute(query)

      query = """
      CREATE TABLE MOUNTED_SPORTSMEN (
            ID SERIAL PRIMARY KEY,
            NAME CHARACTER VARYING(20) NOT NULL,
            SURNAME CHARACTER VARYING(30) NOT NULL,
            BIRTH_YEAR INTEGER ,
            COUNTRY_ID INTEGER NOT NULL REFERENCES COUNTRIES
      )"""
      cursor.execute(query)

In initialize_database function first if the table exists we drop it and than we create the table as new.

Display and Search
^^^^^^^^^^^^^^^^^^

.. code-block:: python

      if request.method == 'GET' or justSearch:
            query="""SELECT * FROM countries"""
            cursor.execute(query)
            countries=cursor.fetchall()
            now = datetime.datetime.now()
            thisYear=datetime.datetime.today().year
            query="""SELECT * FROM MOUNTED_SPORTSMEN"""
            cursor.execute(query)
            allMountedArchers=MountedCollection()
            for row in cursor:
                  id, name, surname, birth_year, country_id = row
                  allMountedArchers.addMountedArcher(MountedArcher(id, name, surname, birth_year, country_id))
            foundMountedArcherCol=MountedCollection()
            if 'search' in request.form:
                  st="""SELECT * FROM MOUNTED_SPORTSMEN WHERE ("""+request.form['filter_by']+"""=%s)"""
                  searchText=request.form['text']
                  if request.form['filter_by'] == "birth_year":
                        searchText=datetime.datetime.today().year-int(request.form['text'])
                  cursor.execute(st, (searchText,))
                  for row in cursor:
                        id, name, surname, birth_year, country_id = row
                        foundMountedArcherCol.addMountedArcher(MountedArcher(id, name, surname, birth_year, country_id))
            cursor.close()
            return render_template('mounted.html', mountedArchers=allMountedArchers.getMountedArchers(), searchMountedArchers=foundMountedArcherCol.getMountedArchers(), allCountries=countries, current_time=now.ctime(), rec_Message=messageToShow, current_year=thisYear)

If the operation is search or we are just displaying information from the database the code above is run.

For displaying we get all the information fro the table with the """SELECT * FROM MOUNTED_SPORTSMEN""" query. And we go through all rows with a loop and send the information to the page.

For searching we use the following query """SELECT * FROM MOUNTED_SPORTSMEN WHERE ("""+request.form['filter_by']+"""=%s)""". This query select all of the information for the the filter we choose. Then we send the selected information to the page.

Delete
^^^^^^

.. code-block:: python

      elif 'mounted_archers_to_delete' in request.form:
            keys = request.form.getlist('mounted_archers_to_delete')
            for key in keys:
                  query="""DELETE FROM MOUNTED_SPORTSMEN WHERE (ID=%s)"""
                  cursor.execute(query, (key,))
            connection.commit()
            cursor.close()
            session['ecb_message']="Successfully deleted!"
            return redirect(url_for('mounted_page'))

If any checkbox (for delete operation) is selected in the form we go through the database and delete the selected rows with the following query """DELETE FROM MOUNTED_SPORTSMEN WHERE (ID=%s)""". %s is the key we took from the form. Then we redirect to mounted archery page.

Insert and Update
^^^^^^^^^^^^^^^^^

.. code-block:: python

      else:
            new_name=request.form['name']
            new_surname=request.form['surname']
            new_age=request.form['age']
            new_country_id=request.form['country_id']
            new_birth_year=datetime.datetime.today().year-int(float(new_age))
            action=request.form['action']
            try:
                  query="""SELECT * FROM MOUNTED_SPORTSMEN WHERE (NAME=%s) AND (SURNAME=%s)"""
                  cursor.execute(query, (new_name, new_surname))
                  mounted_archer=cursor.fetchone()
                  if mounted_archer is not None:
                        session['ecb_message']="Sorry, this archer already exists."
                  elif 'mounted_archer_to_update' in request.form and action=='Update': #update
                        mountedArcherID=request.form.get('mounted_archer_to_update')
                        query="""UPDATE MOUNTED_SPORTSMEN SET (NAME, SURNAME, BIRTH_YEAR, COUNTRY_ID)=(%s, %s, %s, %s) WHERE (ID=%s)"""
                        cursor.execute(query, (new_name, new_surname, new_birth_year, new_country_id, mountedArcherID))
                        connection.commit()
                        session['ecb_message']="Update successfull!"
                  elif action=='Update':
                        session['ecb_message']="Nothing is selected to update!"
                  else:
                        query="""INSERT INTO MOUNTED_SPORTSMEN (NAME, SURNAME, BIRTH_YEAR, COUNTRY_ID) VALUES(%s, %s, %s, %s)"""
                        cursor.execute(query, (new_name, new_surname, new_birth_year, new_country_id))
                        connection.commit()
                        session['ecb_message']="Insertion successfull!"
            except dbapi2.DatabaseError:
                  connection.rollback()
                  session['ecb_message']="Registration failed due to a Database Error."
      return redirect(url_for('mounted_page'))

First we get all of the information from the input tags in the html. Then we try to update or insert.

We look if the there is a person with the same name and surname in the table. If there is we change the error message and end. If not we continue for the update control. If update is requested we use """UPDATE MOUNTED_SPORTSMEN SET (NAME, SURNAME, BIRTH_YEAR, COUNTRY_ID)=(%s, %s, %s, %s) WHERE (ID=%s)""" query to update the old data. If none of the radio button is selected but update button is clicked we give an error message says "Nothing is selected to update!".

If no update requested that mean it is an insert request. So we insert the data with """INSERT INTO MOUNTED_SPORTSMEN (NAME, SURNAME, BIRTH_YEAR, COUNTRY_ID) VALUES(%s, %s, %s, %s)""" query.

Then we have rhe exception handler for database originated errors.
At the end we redirect to the mounted archery page.


Tournament Table
----------------

Creating
^^^^^^^^

Below is the TOURNAMENT table;

+-----------------+-----------------------+--------------+
| Name            | Type                  | Restrictions |
+=================+=======================+==============+
| ID              | integer               | Primary key  |
+-----------------+-----------------------+--------------+
| NAME            | character varying(50) | Not null     |
+-----------------+-----------------------+--------------+
| COUNTRY_ID      | integer               | Foreign key, |
|                 |                       | Not null     |
+-----------------+-----------------------+--------------+
| YEAR            | integer               |              |
+-----------------+-----------------------+--------------+

COUNTRY_ID references to countries table

.. code-block:: sql

      query = """ DROP TABLE IF EXISTS TOURNAMENT"""
      cursor.execute(query)

      query="""CREATE TABLE TOURNAMENT(
            ID SERIAL PRIMARY KEY,
            NAME CHARACTER VARYING(50) NOT NULL,
            COUNTRY_ID INTEGER NOT NULL REFERENCES COUNTRIES,
            YEAR INTEGER
      )"""
      cursor.execute(query)

In initialize_database function first if the table exists we drop it and than we create the table as new.

Display
^^^^^^^

.. code-block:: python

      if request.method == 'GET':
            query="""SELECT * FROM countries"""
            cursor.execute(query)
            countries=cursor.fetchall()
            now = datetime.datetime.now()
            thisYear=datetime.datetime.today().year
            query="""SELECT * FROM TOURNAMENT"""
            cursor.execute(query)
            allTournaments=TournamentCol()
            for row in cursor:
                  id, name, country_id, year = row
                  allTournaments.add_tournament(Tournament(id, name, country_id, year))
            return render_template('tournament.html', tournaments=allTournaments.get_tournaments(), allCountries=countries, current_time=now.ctime(), rec_Message=messageToShow, current_year=thisYear)

To display the information we get the infromation from countries and tournament tables with the select queries. Then we create the objects for each row. Then this object are sent to the page.

Delete
^^^^^^

.. code-block:: python

      elif 'tournaments_to_delete' in request.form:
            keys = request.form.getlist('tournaments_to_delete')
            for key in keys:
                  query="""DELETE FROM TOURNAMENT WHERE (ID=%s)"""
                  cursor.execute(query, (key,))
            connection.commit()
            session['ecb_message']="Successfully deleted!"
            return redirect(url_for('tournament_page'))

If any checkbox (for delete operation) is selected in the form we go through the database and delete the selected rows with the following query """DELETE FROM TOURNAMENT WHERE (ID=%s)""". %s is the key we took from the form. Then we redirect to the tournaments page.

Insert and Update
^^^^^^^^^^^^^^^^^

.. code-block:: python

      else:
            new_name=request.form['name']
            new_country_id=request.form['country_id']
            new_year=request.form['year']
            action=request.form['action']
            try:
                  query="""SELECT * FROM TOURNAMENT WHERE (NAME=%s) AND (COUNTRY_ID=%s) AND (YEAR=%s)"""
                  cursor.execute(query, (new_name, new_country_id, new_year))
                  tournament=cursor.fetchone()
                  if tournament is not None:
                  session['ecb_message']="Sorry, this tournament already exists."
                  elif 'tournament_to_update' in request.form and action=='Update': #update
                        tournamentID=request.form.get('tournament_to_update')
                        query="""UPDATE TOURNAMENT SET (NAME, COUNTRY_ID, YEAR)=(%s, %s, %s) WHERE (ID=%s)"""
                        cursor.execute(query, (new_name, new_country_id, new_year, tournamentID))
                        connection.commit()
                        session['ecb_message']="Update successfull!"
                  elif action=='Update':
                        session['ecb_message']="Nothing is selected to update!"
                  else:
                        query="""INSERT INTO TOURNAMENT (NAME, COUNTRY_ID, YEAR) VALUES(%s, %s, %s)"""
                        cursor.execute(query, (new_name, new_country_id, new_year))
                        connection.commit()
                        session['ecb_message']="Insertion successfull!"
            except dbapi2.DatabaseError:
                  connection.rollback()
                  session['ecb_message']="Registration failed due to a Database Error."
      return redirect(url_for('tournament_page'))

First we star with getting the information from the html input tags. Then we look if the tournament already exists in the tournament table with the """SELECT * FROM TOURNAMENT WHERE (NAME=%s) AND (COUNTRY_ID=%s) AND (YEAR=%s)""" query. If it exists we change the error message to "Sorry, this tournament already exists.".

If it doesn't exists we look for if it is an update request or not. If there is an update request in the form we update the selected row with """UPDATE TOURNAMENT SET (NAME, COUNTRY_ID, YEAR)=(%s, %s, %s) WHERE (ID=%s)""" query.

If no update request that means it is an insert request. Then we insert with the """INSERT INTO TOURNAMENT (NAME, COUNTRY_ID, YEAR) VALUES(%s, %s, %s)""" query.

The messages are updated in all cases. Then we have the exception handler for the database originated errors. At the end we redirect to the tournaments page.


Recurve Scores Table
--------------------

Creating
^^^^^^^^

Below is the SCORE table;

+-----------------+-----------------------+---------------------+
| Name            | Type                  | Restrictions        |
+=================+=======================+=====================+
| ID              | integer               | Primary key         |
+-----------------+-----------------------+---------------------+
| ARCHER_ID       | integer               | Foreign key, Unique |
+-----------------+-----------------------+---------------------+
| TOURNAMENT_ID   | integer               | Foreign key, Unique |
+-----------------+-----------------------+---------------------+
| SCORE           | integer               |                     |
+-----------------+-----------------------+---------------------+

ARCHER_ID references to recurve_sportsmen table

TOURNAMENT_ID references to TOURNAMENT table

.. code-block:: sql

      query = """DROP TABLE IF EXISTS SCORE"""
      cursor.execute(query)

      query = """CREATE TABLE SCORE (
            ID SERIAL PRIMARY KEY,
            ARCHERID INTEGER REFERENCES recurve_sportsmen ON DELETE CASCADE ON UPDATE CASCADE,
            TOURNAMENTID INTEGER REFERENCES TOURNAMENT ON DELETE CASCADE ON UPDATE CASCADE,
            SCORE INTEGER,
            UNIQUE (ARCHERID, TOURNAMENTID)
      )"""
      cursor.execute(query)

In initialize_database function first if the table exists we drop it and than we create the table as new.

Display
^^^^^^^

.. code-block:: python

      if request.method == 'GET':
            query = """SELECT ID, ARCHERID, TOURNAMENTID, SCORE FROM SCORE"""
            cursor.execute(query)
            s = ScoreCol()
            for row in cursor:
                id, archer_id, tournament_id, score = row
                s.add_score(Score(id, archer_id,tournament_id,score))
            scores = s.get_scores()
            now = datetime.datetime.now()
            return render_template('scores.html', current_time=now.ctime(), scores=scores, rec_Message=messageToShow)

To display the information we get the infromation scroe table with the select query. """SELECT ID, ARCHERID, TOURNAMENTID, SCORE FROM SCORE"""
Then we create the objects for each row. Then this object are sent to the page.

Delete
^^^^^^

.. code-block:: python

      elif 'scores_to_delete' in request.form:
            keys = request.form.getlist('scores_to_delete')
            for key in keys:
                query = """DELETE FROM SCORE WHERE (ID = %s)"""
                cursor.execute(query,(key))
            connection.commit()
            session['ecb_message']="Successfully deleted!"
            return redirect(url_for('scores_page'))

If any checkbox (for delete operation) is selected in the form we go through the database and delete the selected rows with the following query """DELETE FROM SCORE WHERE (ID = %s)""". %s is the key we took from the form. Then we redirect to the scores page.

Insert and Update
^^^^^^^^^^^^^^^^^

.. code-block:: python

      else:
            archer_id = request.form['archer_id']
            tournament_id = request.form['tournament_id']
            score = request.form['score']
            action = request.form['action']
            try:
                  query="""SELECT id FROM recurve_sportsmen WHERE (id=%s)"""
                  cursor.execute(query, (archer_id,))
                  archer=cursor.fetchone()
                  query="""SELECT ID FROM TOURNAMENT WHERE (ID=%s)"""
                  cursor.execute(query, (tournament_id,))
                  tournament=cursor.fetchone()
                  if archer is None or tournament is None:
                        session['ecb_message']="Archer or the Tournament is not in our database! Check if they both exists in database."
                        return redirect(url_for('scores_page'))
                  query="""SELECT * FROM SCORE WHERE (ARCHERID=%s) AND (TOURNAMENTID=%s)"""
                  cursor.execute(query, (archer_id, tournament_id))
                  s=cursor.fetchone()
                  if action=='Update':
                        if 'score_to_update' in request.form:
                              scoreID=request.form.get('score_to_update')
                              if s is None or (s is not None and s[0]==int(scoreID)):
                                    query="""UPDATE SCORE SET (ARCHERID, TOURNAMENTID, SCORE)=(%s, %s, %s) WHERE (ID=%s)"""
                                    cursor.execute(query, (archer_id, tournament_id, score, scoreID))
                                    connection.commit()
                                    session['ecb_message']="Update successfull!"
                              else:
                                    session['ecb_message']="Sorry, this specific score already exists."
                        else:
                              session['ecb_message']="Nothing is selected to update!"
                  else:
                        if s is not None:
                              session['ecb_message']="Sorry, this specific score already exists."
                        else:
                              query = """INSERT INTO SCORE (ARCHERID, TOURNAMENTID, SCORE) VALUES (%s,%s,%s)"""
                              cursor.execute(query,(archer_id,tournament_id,score))
                              connection.commit()
                              session['ecb_message']="Insertion successfull!"
            except dbapi2.DatabaseError:
                  connection.rollback()
                  session['ecb_message']="Registration failed due to a Database Error."
      return redirect(url_for('scores_page'))

First we get the information from the html input tags. Then we look if the references exists. We look to the recurve_sportsmen table if archer_id exists and we look to the tournaments table if tournament_id exists. If one of the doesn't exists we change the error message to "Archer or the Tournament is not in our database! Check if they both exists in database." and redirect to the scores page.

If they both exist we look if this input exists in the score table. If it doesn't exists we look for the update request. When there is a update request we update with the """UPDATE SCORE SET (ARCHERID, TOURNAMENTID, SCORE)=(%s, %s, %s) WHERE (ID=%s)""" query. I not we insert with the """INSERT INTO SCORE (ARCHERID, TOURNAMENTID, SCORE) VALUES (%s,%s,%s)""" query. If the row exists in the score table we give the error message "Sorry, this specific score already exists." in these controls.

Then we have the exception handler. After that we redirect to the scores page.


