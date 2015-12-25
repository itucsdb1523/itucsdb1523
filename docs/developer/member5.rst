Parts Implemented by Member Emre Kerem ORGUN
============================================

1. `Compound Sportsmen Table`_
2. `Sponsors Page Table`_
3. `Compound Team Page`_
4. `Compound Team Members`_

Compound Sportsmen Table
------------------------

 Compound Sportsmen Table is designed for sportmen records as per Name, Last Name, Age and Nationality.

+-----------+-------------------+--------------+
| Name      | Type              | Restrictions |
+===========+===================+==============+
| ID        | integer           | Primary key  |
+-----------+-------------------+--------------+
| Name      | character varying |              |
+-----------+-------------------+--------------+
| Last Name | character varying |              |
+-----------+-------------------+--------------+
| Age       | integer           |              |
+-----------+-------------------+--------------+
| CountryID | integer           | Foreign key  |
+-----------+-------------------+--------------+


*Information
   * *CountryID* is references Countries table

The creation of database is like below:

.. code-block:: sql

      DROP TABLE IF EXISTS COMPOUNDSPORTSMEN
      CREATE TABLE CompoundSportsmen (
           ID serial PRIMARY KEY,
           Name character varying(20) NOT NULL,
           LastName character varying(30) NOT NULL,
           BirthYear integer,
           CountryID integer NOT NULL references countries(id)
           )



Connection of Database
++++++++++++++++++++++

* Initializing database and connecting them codes are below. Request method gets countries and  CompoundSportsmen tables.
* To calculate age of the sportsmen, date datetime is calculated.
* Values are get by request method assigned to defined attributes in row.
* It is returned to html page at the end.

.. code-block:: python

      @app.route('/compound_archery', methods=['GET', 'POST'])
      def compound_page():
      with dbapi2.connect(app.config['dsn']) as connection:
        cursor=connection.cursor()
        messageToShow=""
      #display compounders
      if request.method == 'GET':
        statement="""SELECT * FROM countries"""
        cursor.execute(statement)
        countries=cursor.fetchall()
        now = datetime.datetime.now()
        thisYear=datetime.datetime.today().year
        statement="""SELECT * FROM CompoundSportsmen"""
        cursor.execute(statement)
        allCompounders=CompoundCollection()
        for row in cursor:
            ID, Name, LastName, BirthYear, CountryID = row
            allCompounders.add_compounder(Compounder(ID, Name, LastName, BirthYear,
                                           CountryID))
        cursor.close()
        return render_template('compound.html',
             compounders=allCompounders.get_compounders(),
               allCountries=countries, current_time=now.ctime(),
                rec_Message=messageToShow, current_year=thisYear)



*  *compounders_to_delete* is the name of the column called 'delete column' has checkboxes that is defined to connect.
* If user select the checkbox and click the delete button, records will be deleted in terms of ID.
* Session warns user either successful or unsuccessful and redirected to page again.

.. code-block:: python

   elif 'compounders_to_delete' in request.form:
        keys = request.form.getlist('compounders_to_delete')
        for key in keys:
            statement="""DELETE FROM CompoundSportsmen WHERE (ID=%s)"""
            cursor.execute(statement, (key,))
        connection.commit()
        cursor.close()
        session['message']="Successfully deleted!"
        return redirect(url_for('compound_page'))



* To get new values and add or update operation, new attributes block is defined.
* By using datetime, sportsmen's age is updated automatically over the years.

.. code-block:: python

    else:
        new_name=request.form['Name']
        new_surname=request.form['LastName']
        new_age=request.form['age']
        new_country_id=request.form['country_id']
        new_birth_year=datetime.datetime.today().year-int(float(new_age))

* According to name and last name, it is tried to understand whether sportsmen is already recorded or not.
* If sportsmen is recorded, user is warned.
* If not
      * 1. Update radiobox is clicked and data is given, records will be updated.
      * 2.  Values are given and clicked add button, record will be inserted.

.. code-block:: python

    try:
      statement="""SELECT * FROM CompoundSportsmen WHERE (NAME=%s) AND (LASTNAME=%s)"""
      cursor.execute(statement, (new_name, new_surname))
      compounder=cursor.fetchone()
      if compounder is not None:
          session['message']="Sorry, this compound sportsman already exists."
          cursor.close()
          connection.close()
          return redirect(url_for('compound_page'))
      elif 'compounder_to_update' in request.form:
          session['message']="Update successfull!"
          compounderID=request.form.get('compounder_to_update')
          statement="""UPDATE compoundsportsmen SET (name, lastname, birthyear, countryid)
                                                =(%s, %s, %s, %s) WHERE (ID=%s)"""
          cursor.execute(statement, (new_name, new_surname, new_birth_year, new_country_id,
                                       compounderID))
          connection.commit()
      else: #try to insert
       statement="""INSERT INTO CompoundSportsmen (Name, Lastname, BirthYear, CountryID)
                                 VALUES(%s, %s, %s, %s)"""
       cursor.execute(statement, (new_name, new_surname, new_birth_year, new_country_id))
       connection.commit()
   except dbapi2.DatabaseError:
      connection.rollback()
      session['message']="Registration failed due to a Database Error."

* At the end, connection is closed.

.. code-block:: python

    cursor.close()
    connection.close()
    return redirect(url_for('compound_page'))


Sponsors Page Table
-------------------



Sponsors table
++++++++++++++


 * Sponsors Table is designed for sponsor records as per Name, year, Budget and Nationality.


+-------------+-------------------+--------------+
| Name        | Type              | Restrictions |
+=============+===================+==============+
| ID          | integer           | Primary key  |
+-------------+-------------------+--------------+
| SponsorName | character varying |              |
+-------------+-------------------+--------------+
| Year        | integer           |              |
+-------------+-------------------+--------------+
| Budget      | integer           |              |
+-------------+-------------------+--------------+
| CountryID   | integer           | Foreign key  |
+-------------+-------------------+--------------+


*Information
   * *CountryID* is references Countries table

The creation of database is like below:

.. code-block:: python

   CREATE TABLE Sponsors (
        ID serial PRIMARY KEY,
        SponsorName character varying(50) NOT NULL,
        budget integer,
        year integer,
        CountryID integer NOT NULL references countries(id)
        )




Connection of Database
++++++++++++++++++++++

* Initializing database and connecting them codes are below. Request method gets countries and  Sponsors tables.
* Values are get by request method assigned to defined attributes in row.
* It is returned to html page at the end.

.. code-block:: python

   @app.route('/Sponsors', methods=['GET', 'POST'])
   def sponsors_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor=connection.cursor()
        messageToShow=""
    if request.method == 'GET':
        statement="""SELECT * FROM Countries"""
        cursor.execute(statement)
        countries=cursor.fetchall()
        now = datetime.datetime.now()
        thisYear=datetime.datetime.today().year
        statement="""SELECT * FROM Sponsors"""
        cursor.execute(statement)
        allSponsors=SponsorCollection()
        for row in cursor:
            ID, SponsorName, year, budget, CountryID = row
            allSponsors.add_sponsor(Sponsor(ID, SponsorName,year, budget,
                                     CountryID))
        cursor.close()
        return render_template('sponsors.html',sponsors=allSponsors.get_sponsors(),
           allCountries=countries, current_year=thisYear, current_time=now.ctime(),
                rec_Message=messageToShow,)


*  *sponsors_to_delete* is the name of the column called 'delete column' has checkboxes that is defined to connect.
* If user select the checkbox and click the delete button, records will be deleted in terms of ID.
* Session warns user either successful or unsuccessful and redirected to page again.

.. code-block:: python

   elif 'sponsors_to_delete' in request.form:
        keys = request.form.getlist('sponsors_to_delete')
        for key in keys:
            statement="""DELETE FROM Sponsors WHERE (ID=%s)"""
            cursor.execute(statement, (key,))
        connection.commit()
        cursor.close()
        session['message']="Successfully deleted!"
        return redirect(url_for('sponsors_page'))

* To get new values and add or update operation, new attributes block is defined.

.. code-block:: python

        new_name=request.form['SponsorName']
        new_budget=request.form['budget']
        new_year=request.form['year']
        new_country_id=request.form['country_id']



* According to name, it is tried to understand whether sponsor is already recorded or not.
* If sponsor is recorded, user is warned.
* If not
      * 1.  Update radiobox is clicked and data is given, records will be updated.
      * 2.  Values are given and clicked add button, record will be inserted.

.. code-block:: python

   try:
         statement="""SELECT * FROM Sponsors WHERE (SponsorNAME=%s)"""
         cursor.execute(statement, (new_name,))
         sponsor=cursor.fetchone()
         if sponsor is not None:
             session['message']="Sorry, this sponsor already exists."
             cursor.close()
             connection.close()
             return redirect(url_for('sponsors_page'))
         elif 'sponsor_to_update' in request.form:
             session['message']="Update successfull!"
             sponsorID=request.form.get('sponsor_to_update')
             statement="""UPDATE sponsors SET (sponsorname, year, budget, countryid)=
                           (%s, %s, %s, %s) WHERE (ID=%s)"""
             cursor.execute(statement, (new_name, new_year,new_budget,
                                        new_country_id, sponsorID))
             connection.commit()
         else: #try to insert
             statement="""INSERT INTO Sponsors (SponsorName, budget, year, CountryID)
                            VALUES(%s, %s, %s, %s)"""
             cursor.execute(statement, (new_name, new_budget, new_year,
                              new_country_id))
             connection.commit()
     except dbapi2.DatabaseError:
         connection.rollback()
         session['message']="Registration failed due to a Database Error."





* At the end, connection is closed.
.. code-block:: python

    cursor.close()
    connection.close()
    return redirect(url_for('sponsors_page'))





Compound Team Page
------------------


+-------------+-------------------+--------------+
| Name        | Type              | Restrictions |
+=============+===================+==============+
| ID          | integer           | Primary key  |
+-------------+-------------------+--------------+
| TeamName    | character varying |              |
+-------------+-------------------+--------------+
| ContactTeam | character varying |              |
+-------------+-------------------+--------------+

*Compound_data table is created.


.. code-block:: python

    CREATE TABLE compound_data (
            id serial PRIMARY KEY,
            compound_team character varying(30) NOT NULL,
            compound_contact character varying(30)
        )

*Database connection is initialized.

.. code-block:: python

   @app.route('/compound_teams', methods=['GET', 'POST'])
   def compoundteams_page():
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor=connection.cursor()
        if 'message' in session:
            messageToShow=session['message']
            session['message']=""
        else:
            messageToShow=""

*SQL queries are done to make HTML file functional.

.. code-block:: python

   if request.method == 'GET':
      statement="""SELECT * FROM compoundsportsmen"""
      cursor.execute(statement)
      allCompounders=CompoundCollection()
      for row in cursor:
          ID, Name, Lastname, BirthYear, CountryID = row
          allCompounders.add_compounder(Compounder(ID, Name, Lastname, BirthYear,
                                          CountryID))
      statement="""SELECT * FROM compound_data"""
      cursor.execute(statement)
      allTeams=CompoundTeamCollection()
      for row in cursor:
          id, compound_team, compound_contact = row
          allTeams.add_compoundteam(CompoundTeam(id, compound_team, compound_contact))
      return render_template('compoundteam.html',
                              compounders=allCompounders.get_compounders(),
                               recTableMessage=messageToShow,
                                compoundteams=allTeams.get_compoundteams())

*Insetion of Compound Team

.. code-block:: python

       elif 'insert' in request.form:
            compound_team = request.form['inputName']
            compound_contact = request.form['inputlink']
            statement="""SELECT * FROM compound_data
                           WHERE (compound_team=%s)"""
            cursor.execute(statement, (compound_team,))
            Ifthereissame=cursor.fetchone()



.. code-block:: python

   if Ifthereissame is not None:
        cursor.close()
        return redirect(url_for('compoundteams_page'))

   else: #insert new team
       statement="""INSERT INTO compound_data (compound_team, compound_contact)
                      VALUES(%s, %s)"""
       cursor.execute(statement, (compound_team, compound_contact))
       connection.commit()
       return redirect(url_for('compoundteams_page'))

*A member is inserted to the team

.. code-block:: python

   elif 'insertMember' in request.form:
      compoundteam_id=request.form['dd_team_id']
      compound_member=request.form['compound_member']
      statement="""SELECT count(*) FROM compoundteam
                     WHERE (compoundteam_ID=%s)"""
      cursor.execute(statement, (compoundteam_id,))
      resultCount=cursor.fetchone()
      if resultCount[0] == 3: #team is full
          session['message']="Sorry, the team is full."
          cursor.close()
          return redirect(url_for('compoundteams_page'))
      statement="""SELECT * FROM compoundteam
                     WHERE (compounder_id=%s)"""
      cursor.execute(statement, (compound_member,))
      memberInTeam=cursor.fetchone()
      if memberInTeam is not None:
          cursor.close()
      else: #insert
          statement="""INSERT INTO compoundteam (compoundteam_id, compounder_id)
                         VALUES(%s, %s)"""
          cursor.execute(statement, (compoundteam_id, compound_member))
          connection.commit()
          session['message']="The compound archer has joined to the team."
          cursor.close()
      return redirect(url_for('compoundteams_page'))

*Deletion operation is done.

.. code-block:: python

   elif 'compoundteams_to_delete' in request.form:
            keys = request.form.getlist('compoundteams_to_delete')
            for key in keys:
                statement="""DELETE FROM compound_data WHERE (id=%s)"""
                cursor.execute(statement, (key,))
            connection.commit()
            cursor.close()
            session['ecb_message']="Successfully deleted!"
            return redirect(url_for('compoundteams_page'))


Compound Team Members
---------------------


+-----------------+---------+--------------+
| Name            | Type    | Restrictions |
+=================+=========+==============+
| ID              | integer | Primary key  |
+-----------------+---------+--------------+
| compoundteam_id | integer | Foreign key  |
+-----------------+---------+--------------+
| compounder_id   | integer | Foreign key  |
+-----------------+---------+--------------+

*Compound team table is created.

.. code-block:: python

   DROP TABLE IF EXISTS COMPOUNDTEAM
   CREATE TABLE COMPOUNDTEAM (
            id serial PRIMARY KEY,
            compoundteam_id integer NOT NULL references compound_data(id)
                         ON DELETE CASCADE ON UPDATE CASCADE,
            compounder_id integer NOT NULL references compoundsportsmen(id)
                         ON DELETE CASCADE ON UPDATE CASCADE
            )

*Database connection is done.

.. code-block:: python

   @app.route('/compound_team/<int:key>', methods=['GET', 'POST'])
   def compoundteam_page(key):
    with dbapi2.connect(app.config['dsn']) as connection:
        cursor=connection.cursor()
        cursor2=connection.cursor()
        if 'message' in session:
            messageToShow=session['message']
            session['message']=""
        else:
            messageToShow=""

*Compound team members are listed in HTML file appropriately.

.. code-block:: python

   if request.method == 'GET':
      statement="""SELECT * FROM countries"""
      cursor.execute(statement)
      countries=cursor.fetchall()
      statement="""SELECT * FROM compound_data WHERE (id=%s)"""
      cursor.execute(statement, (key,))
      catchInfo=cursor.fetchone()
      theTeam=CompoundTeam(catchInfo[0], catchInfo[1], catchInfo[2])
      thisYear = datetime.datetime.today().year
      statement="""SELECT * FROM compoundteam WHERE (id=%s)"""
      cursor.execute(statement, (key,))
      CompoundersInTeam = CompoundCollection()
      for row in cursor:
          id, compoundteam_id, compounder_id = row
          statement="""SELECT * FROM compoundsportsmen WHERE (id=%s)"""
          cursor2.execute(statement, (compounder_id,))
          Compound=cursor2.fetchone()
          CompoundersInTeam.add_compounder(Compounder(Compound[0], Compound[1],
                            Compound[2],Compound[3], Compound[4]))
      return render_template('compoundteam_member.html',
          compounders=CompoundersInTeam.get_compounders(),
             recTableMessage=messageToShow, compoundteam=theTeam,
                current_year=thisYear, allCountries=countries)

*Deletion operation for compounders from team

.. code-block:: python

   elif 'compounders_to_delete' in request.form:
            keys = request.form.getlist('compounders_to_delete')
            for element in keys:
                statement="""DELETE FROM compoundteam
                              WHERE (compounder_id=%s)"""
                cursor.execute(statement, (element,))
            connection.commit()
            cursor.close()
            session['ecb_message']="Succesfully deleted"
            return redirect(url_for('compoundteam_page', key=key))

*At the and returned to the page.

.. code-block:: python

   else:
            return redirect(url_for('compoundteam_page', key=key))



