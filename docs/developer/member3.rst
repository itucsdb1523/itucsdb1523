Parts Implemented by Mehmet Arif Cengiz
***************************************

Developer Manual of Pages
=========================

1. `Competitions Page`_
2. `Archery Clubs Page`_
3. `Informations Page`_

Competitions Page
-----------------

Features of Competition Table
+++++++++++++++++++++++++++++

* Competitions table is created for *Archery Competitions* with respect to different types of archery, year and country.

+-----------------+-------------------+--------------+
| Name            | Type              | Restrictions |
+=================+===================+==============+
| ID              | integer           | Primary key  |
+-----------------+-------------------+--------------+
| CompetitionName | character varying |              |
+-----------------+-------------------+--------------+
| CompType        | character varying |              |
+-----------------+-------------------+--------------+
| Year            | integer           |              |
+-----------------+-------------------+--------------+
| CountryID       | integer           | Foreign key  |
+-----------------+-------------------+--------------+

*Information
   * *CountryID* is references Countries table

The structure of table is like below:

.. code-block:: sql

         DROP TABLE IF EXISTS COMPETITIONS;
         CREATE TABLE COMPETITIONS
         (
            ID SERIAL PRIMARY KEY,
            CompetitionName character varying(200),
            CompType character varying(100),
            Year INTEGER,
            CountryID INTEGER NOT NULL references countries(id)
         )


Connection of Competition Table
+++++++++++++++++++++++++++++++

.. code-block:: python

         @app.route('/achery_competition', methods=['GET', 'POST'])
         def competition_page():
            with dbapi2.connect(app.config['dsn']) as connection:
                 cursor=connection.cursor()



Connection of Countries Reference
+++++++++++++++++++++++++++++++++

* The code block below provides to access table of countries to connect them tuples.

.. code-block:: python

            request.method == 'GET':
               statement="""SELECT * FROM countries"""
                 cursor.execute(statement)
                  countries=cursor.fetchall()



Connection of Competitions Records
++++++++++++++++++++++++++++++++++


  *  The code below provides to achieve records in competitions table. If there are some records in table, user can reach these otherwise empty table is returned on html page.

.. code-block:: python

      statement="""SELECT * FROM Competitions"""
      cursor.execute(statement)
      allCompetitions=CompetitionCollection()
      for row in cursor:
          ID, CompetitionName, CompType, Year, CountryID = row
          allCompetitions.add_competition(Competition(ID, CompetitionName, CompType, Year, CountryID ))
      cursor.close()
      return render_template('competitions.html', competitions = allCompetitions.get_competitions(),
                              allCountries=countries, rec_Message=messageToShow)


Operations of Competition Table
+++++++++++++++++++++++++++++++

   *Delete Operation*

.. code-block:: html

  <td><input type="checkbox" name="competitions_to_delete" value="{{competition.ID}}" /></td>


* Record will be deleted is selected by clicking checkbox on html. *competitions_to_delete* is defined checkbox's name to reach in python.
* In the code below, if *competitions_to_delete* is true, sql statement DELETE is executed in terms of ID.
* After that operation, it is redirected to defining fuction on python.

.. code-block:: python

        elif 'competitions_to_delete' in request.form:
          keys = request.form.getlist('competitions_to_delete')
           for key in keys:
               statement="""DELETE FROM competitions WHERE (ID=%s)"""
             cursor.execute(statement, (key,))
         connection.commit()
         cursor.close()
         return redirect(url_for('competition_page'))


  *Creating New Attributes*

*  Adding a new record or updating a record require new attributes to assign new values on old records. Because of that, new attributes assigned to html table cells.

.. code-block:: python

         new_compname=request.form['CompetitionName']
         new_type=request.form['CompType']
         new_year1=request.form['Year']
          new_country_id=request.form['CountryID']


* The values that entered are assigned to *new* attributes to try add or update values.

.. code-block:: python

   statement="""SELECT * FROM Competitions WHERE (CompetitionName=%s) AND (CompType=%s) AND
                                                 (Year=%s) AND (CountryID=%s)"""
   cursor.execute(statement, (new_compname, new_type,new_year1,new_country_id))
   competition=cursor.fetchone()


* The values that are entered above make no sense if there is any record same. The code below provides the control and if there a record same as entered, warning message send.
* After that, it is returned to function.

.. code-block:: python

         if competition is not None:
                messageToShow="competitions already exist"
                cursor.close()
                connection.close()
                return redirect(url_for('competition_page'))


*Update Operation*

.. code-block:: html

    <td><input type="radio" name="competitions_to_update" value="{{competition.ID}}" form="form1"/></td>

* Update operation is selected by clicking radio button on html. *competitions_to_update* is assigned as name of radiobox to reach it with python.
* All the blanks should filled with clicking the radiobox to update values.
* In the code below, if *competitions_to_update* is true, sql statement UPDATE is executed in terms of all values.

.. code-block:: python

   elif 'competitions_to_update' in request.form:
      competitionID = request.form.get('competitions_to_update')
      statement = """UPDATE competitions SET (CompetitionName, CompType, Year, CountryID)=
                                                (%s, %s, %s, %s) WHERE (id=%s)"""
      cursor.execute(statement, (new_compname, new_type, new_year1, new_country_id, competitionID))
      connection.commit()


*  The entered values, that are assigned *new* attributes very above,  is inserted into database with sql statement below
*  After that  values are commited and are written on html page.
*
.. code-block:: python

    else: #try to insert
      statement="""INSERT INTO Competitions (CompetitionName, CompType, Year, CountryID) VALUES
                                                (%s, %s, %s, %s)"""
      cursor.execute(statement, (new_compname, new_type, new_year1, new_country_id))
      connection.commit()


* After all, operations are done, connection and cursor are closed, and it is redirected to beginning of the function.

.. code-block:: python

   cursor.close()
    connection.close()
    return redirect(url_for('competition_page'))





Archery Clubs Page
------------------


Features of Archery Clubs Table
+++++++++++++++++++++++++++++++



* Archery Clubs table is created for *Archery Clubs* with respect to different year and country.

+-----------+-------------------+--------------+
| Name      | Type              | Restrictions |
+===========+===================+==============+
| ID        | integer           | Primary key  |
+-----------+-------------------+--------------+
| ClubName  | character varying |              |
+-----------+-------------------+--------------+
| CountryID | integer           | Foreign key  |
+-----------+-------------------+--------------+
| Year      | integer           |              |
+-----------+-------------------+--------------+


*Information
   * *CountryID* is references Countries table

The structure of table is like below:


.. code-block:: sql

   DROP TABLE IF EXISTS ArcheryClubs
   CREATE TABLE ArcheryClubs
   (
            ID SERIAL PRIMARY KEY,
            CLUBNAME CHARACTER VARYING(200),
            COUNTRYID INTEGER NOT NULL references countries(id),
            CLUBYEAR INTEGER
    )


Connection of Archery Clubs Table
+++++++++++++++++++++++++++++++++

.. code-block:: python
   @app.route('/clubs_archery', methods=['GET', 'POST'])
   def archeryclubs_page():
      with dbapi2.connect(app.config['dsn']) as connection:
            cursor=connection.cursor()



Connection of Countries Reference
+++++++++++++++++++++++++++++++++


* The code block below provides to access table of countries to connect them tuples.

.. code-block:: python

            request.method == 'GET':
               statement="""SELECT * FROM countries"""
                 cursor.execute(statement)
                  countries=cursor.fetchall()



Connection of Archery Clubs Records
+++++++++++++++++++++++++++++++++++


  *  The code below provides to achieve records in Archery Clubs table. If there are some records in table, user can reach these otherwise empty table is returned on html page.

.. code-block:: python
   statement="""SELECT * FROM ArcheryClubs"""
        cursor.execute(statement)
        allClubs=ClubCollection()
        for row in cursor:
             ID, ClubName, CountryID, ClubYear = row
             allClubs.add_club(archery_clubs(ID, ClubName, CountryID, ClubYear))
        cursor.close()
        return render_template('arc_clubs.html', clubs=allClubs.get_clubs(),
                                  allCountries=countries, rec_Message=messageToShow)




Operations of Archery Clubs Table
+++++++++++++++++++++++++++++++++

   *Delete Operation*

.. code-block:: html
   <td><input type="checkbox" Name="clubs_to_delete" value="{{club.ID}}" /></td>



* Record will be deleted is selected by clicking checkbox on html. *clubs_to_delete* is defined checkbox's name to reach in python.
* In the code below, if *clubs_to_delete* is true, sql statement DELETE is executed in terms of ID.
* After that operation, it is redirected to defining fuction on python.

.. code-block:: python

        elif 'clubs_to_delete' in request.form:
            keys = request.form.getlist('clubs_to_delete')
            for key in keys:
                  statement="""DELETE FROM ArcheryClubs WHERE (ID=%s)"""
                  cursor.execute(statement, (key,))
             connection.commit()
             cursor.close()

             return redirect(url_for('archeryclubs_page'))


  *Creating New Attributes*

*  Adding a new record or updating a record require new attributes to assign new values on old records. Because of that, new attributes assigned to html table cells.

.. code-block:: python

         new_name=request.form['ClubName']
         new_country_id=request.form['countryid']
         new_year2=request.form['ClubYear']

* The values that entered are assigned to *new* attributes to try add or update values.

.. code-block:: python

      statement="""SELECT * FROM ARcheryClubs WHERE (CLUBNAME=%s) AND (countryid=%s) AND (ClubYear=%s)"""
      cursor.execute(statement, (new_name,new_country_id,new_year2))
      club=cursor.fetchone()


* The values that are entered above make no sense if there is any record same. The code below provides the control and if there a record same as entered, warning message send.
* After that, it is returned to function.

.. code-block:: python

      if club is not None:
             messageToShow="there exists this information"
             cursor.close()
             connection.close()
             return redirect(url_for('archeryclubs_page'))

*Update Operation*

.. code-block:: html

   <td><input type="radio" Name="clubs_to_update" value="{{club.ID}}" form="form1" /></td>

* Update operation is selected by clicking radio button on html. *clubs_to_update* is assigned as name of radiobox to reach it with python.
* All the blanks should filled with clicking the radiobox to update values.
* In the code below, if *clubs_to_update* is true, sql statement UPDATE is executed in terms of all values.

.. code-block:: python

     elif 'clubs_to_update' in request.form:
        clubID=request.form.get('clubs_to_update')
        cursor.execute("""UPDATE archeryclubs SET (clubname,countryid,clubyear)=(%s, %s, %s) WHERE (id=%s)""",
                                                   (new_name,new_country_id,new_year2,clubID))
        connection.commit()


*  The entered values, that are assigned *new* attributes very above,  is inserted into database with sql statement below
*  After that  values are commited and are written on html page.
*
.. code-block:: python

      else:
        statement="""INSERT INTO ArcheryClubs (ClubName, CountryID, ClubYear) VALUES(%s, %s, %s)"""
        cursor.execute(statement, (new_name, new_country_id, new_year2))
        connection.commit()

* After all, operations are done, connection and cursor are closed, and it is redirected to beginning of the function.

.. code-block:: python

   cursor.close()
    connection.close()
    return redirect(url_for('archeryclubs_page'))



Informations Page
-----------------


Features of Informations Table
++++++++++++++++++++++++++++++



* Informations table is created for *Informations* with respect to different name, olympics and year.


+------------+-------------------+--------------+
| Name       | Type              | Restrictions |
+============+===================+==============+
| ID         | integer           | Primary key  |
+------------+-------------------+--------------+
| T_Name     | character varying |              |
+------------+-------------------+--------------+
| T_Olympics | character varying |              |
+------------+-------------------+--------------+
| Year       | integer           |              |
+------------+-------------------+--------------+
| Info       | character varying |              |
+------------+-------------------+--------------+


The structure of table is like below:


.. code-block:: sql

   DROP TABLE IF EXISTS informations
   CREATE TABLE informations
   (
            ID SERIAL PRIMARY KEY,
            T_Name CHARACTER VARYING(200),
            T_Olympics CHARACTER VARYING(200),
            YEAR INTEGER,
            Info CHARACTER VARYING(900)
   )


Connection of Informations Table
++++++++++++++++++++++++++++++++

.. code-block:: python

   @app.route('/Tournament_Information', methods=['GET', 'POST'])
   def tournament_information_page():
       with dbapi2.connect(app.config['dsn']) as connection:
           cursor=connection.cursor()




Connection of Informations Records
++++++++++++++++++++++++++++++++++


  *  The code below provides to achieve records in Informations table. If there are some records in table, user can reach these otherwise empty table is returned on html page.

.. code-block:: python

   statement="""SELECT * FROM informations"""
        cursor.execute(statement)
        allInfos=infoCollection()
        for row in cursor:
             ID, T_Name, T_Olympics, Year, Info = row
             allInfos.add_information(information_class(ID, T_Name, T_Olympics, Year, Info))
        cursor.close()
        return render_template('informations.html', informations=allInfos.get_informations(),
                                  rec_Message=messageToShow)



Operations of Informations Table
++++++++++++++++++++++++++++++++

   *Delete Operation*

.. code-block:: html
    <td><input type="checkbox" Name="informations_to_delete" value="{{information.ID}}" /></td>



* Record will be deleted is selected by clicking checkbox on html. *informations_to_delete* is defined checkbox's name to reach in python.
* In the code below, if *informations_to_delete* is true, sql statement DELETE is executed in terms of ID.
* After that operation, it is redirected to defining fuction on python.

.. code-block:: python

     elif 'informations_to_delete' in request.form:
         keys = request.form.getlist('informations_to_delete')
         for key in keys:
              statement="""DELETE FROM informations WHERE (ID=%s)"""
              cursor.execute(statement, (key,))
         connection.commit()
         cursor.close()

         return redirect(url_for('tournament_information_page'))



  *Creating New Attributes*

*  Adding a new record or updating a record require new attributes to assign new values on old records. Because of that, new attributes assigned to html table cells.

.. code-block:: python

        new_name=request.form['T_Name']
        new_T_Olympics=request.form['T_Olympics']
        new_year3=request.form['Year']
        new_info=request.form['Info']

* The values that entered are assigned to *new* attributes to try add or update values.

.. code-block:: python

      statement="""SELECT * FROM informations WHERE (T_NAME=%s) AND (T_Olympics=%s) AND (Year=%s) AND (Info=%s)"""
      cursor.execute(statement, (new_name,new_T_Olympics,new_year3,new_info))
      information=cursor.fetchone()


* The values that are entered above make no sense if there is any record same. The code below provides the control and if there a record same as entered, warning message send.
* After that, it is returned to function.

.. code-block:: python

      if information is not None:
          messageToShow="there exists this information"
          cursor.close()
          connection.close()
          return redirect(url_for('tournament_information_page'))


*Update Operation*

.. code-block:: html

     <td><input type="radio" Name="informations_to_update" value="{{information.ID}}" form="form1" / ></td>

* Update operation is selected by clicking radio button on html. *informations_to_update* is assigned as name of radiobox to reach it with python.
* All the blanks should filled with clicking the radiobox to update values.
* In the code below, if *informations_to_update* is true, sql statement UPDATE is executed in terms of all values.

.. code-block:: python

     elif 'informations_to_update' in request.form:
        infoID=request.form.get('informations_to_update')
        statement="""UPDATE informations SET (T_name,T_Olympics, Year, info)=(%s, %s, %s, %s) WHERE (id=%s)"""
        cursor.execute(statement,(new_name, new_T_Olympics, new_year3 ,new_info, infoID))
        connection.commit()


*  The entered values, that are assigned *new* attributes very above,  is inserted into database with sql statement below
*  After that  values are commited and are written on html page.
*
.. code-block:: python

      else:
        statement="""INSERT INTO informations (T_name,T_Olympics, Year, Info) VALUES(%s, %s, %s, %s)"""
        cursor.execute(statement, (new_name,new_T_Olympics,new_year3,new_info))
        connection.commit()

* After all, operations are done, connection and cursor are closed, and it is redirected to beginning of the function.

.. code-block:: python

    cursor.close()
    connection.close()
    return redirect(url_for('tournament_information_page'))
