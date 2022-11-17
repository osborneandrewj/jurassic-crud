# Adapted from the excellent starter project at https://github.com/osu-cs340-ecampus/flask-starter-app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from dotenv import load_dotenv, find_dotenv
import os
import database.db_connector as db

# Configuration
app = Flask(__name__)

# Load our environment variables from the .env file in the root of our project.
load_dotenv(find_dotenv())

# database connection info
app.config["MYSQL_HOST"] = os.environ.get("340DBHOST")
app.config["MYSQL_USER"] = os.environ.get("340DBUSER")
app.config["MYSQL_PASSWORD"] = os.environ.get("340DBPW")
app.config["MYSQL_DB"] = os.environ.get("340DB")
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Data used to pre-populate dropdown menus

status_options = ["healthy", "sick", "injured"]

# Routes 

@app.route('/')
def root():
    return redirect("/dinosaurs")

@app.route('/dinosaurs', methods=["POST", "GET"])
def dinosaurs():
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Dinosaurs.id AS 'ID', Dinosaurs.name AS 'Name', Species.species_name AS 'Species', Locations.location_name AS 'Location', Dinosaurs.health_status AS 'Status' FROM Dinosaurs INNER JOIN Species ON Dinosaurs.species_id = Species.id INNER JOIN Locations ON Dinosaurs.location_id = Locations.id"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab data for dropdowns
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()

        # mySQL query to grab data for dropdowns
        species_query = "SELECT species_name from Species;"
        cur = mysql.connection.cursor()
        cur.execute(species_query)
        spec_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("dinosaurs.j2", data=data, locations=loc_data, 
        spec_data=spec_data)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Dinosaur"):
            # grab user form inputs
            species = request.form["species"]
            location = request.form["location"]
            name = request.form["name"]
            status = request.form["status"]

        # TODO: account for null species
            if species == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, name, status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "INSERT INTO Dinosaurs(species_id, location_id, name, health_status)\
                    VALUES((SELECT id FROM Species WHERE species_name= %s),\
                    (SELECT id FROM Locations WHERE location_name= %s), %s,\
                    %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, name, status))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/dinosaurs")

@app.route('/update_dinosaur/<int:id>', methods=["POST", "GET"])
def update_dinosaur(id):
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab a specific dinosaur that the user selected
        query = "SELECT Dinosaurs.id AS 'ID',\
            Dinosaurs.name AS 'Name',\
            Species.species_name AS 'Species',\
            Locations.location_name AS 'Location',\
            Dinosaurs.health_status AS 'Status'\
            FROM Dinosaurs\
                INNER JOIN Species ON Dinosaurs.species_id = Species.id\
                INNER JOIN Locations ON Dinosaurs.location_id = Locations.id WHERE Dinosaurs.id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        # mySQL query to grab data for the location dropdown menu
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()

        # mySQL query to grab data for the species dropdown menu
        species_query = "SELECT species_name from Species;"
        cur = mysql.connection.cursor()
        cur.execute(species_query)
        spec_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("update_dinosaur.j2", 
            data=data, locations=loc_data, 
            spec_data=spec_data, status_options=status_options)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Update_Dinosaur"):
            # grab user form inputs
            species = request.form["species"]
            location = request.form["location"]
            name = request.form["name"]
            status = request.form["status"]

        # TODO: account for null species
            if species == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, name, status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "UPDATE Dinosaurs\
                    SET species_id = (SELECT id FROM Species WHERE species_name=%s),\
                        location_id = (SELECT id FROM Locations WHERE location_name= %s),\
                        name = %s,\
                        health_status = %s\
                    WHERE id = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, name, status, id))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/dinosaurs")

# route for delete functionality, deleting a dinosaur from Dinosaurs,
# we want to pass the 'id' value of that dinosaur on button click 
@app.route("/delete_dinosaur/<int:id>", methods=["POST", "GET"])
def delete_dinosaur(id):

    if request.method == "GET":
        # mysql query to gather the form's data
        query = "SELECT Dinosaurs.id AS 'ID', Dinosaurs.name AS 'Name', Species.species_name AS 'Species', Locations.location_name AS 'Location', Dinosaurs.health_status AS 'Status'\
        FROM Dinosaurs\
            INNER JOIN Species ON Dinosaurs.species_id = Species.id\
            INNER JOIN Locations ON Dinosaurs.location_id = Locations.id WHERE Dinosaurs.id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("delete_dinosaur.j2", data=data)


    if request.method == "POST":
        query = "DELETE FROM Dinosaurs WHERE Dinosaurs.id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to dinosaur page
    return redirect("/dinosaurs")

@app.route('/species')
def species():

    query = "SELECT * FROM Species;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template("species.j2", Species=results)


@app.route('/dinosaurAssignments', methods=["POST", "GET"])
def dinosaurAssignments():
    #insert a dino assignment into the table
    if request.method == 'POST':
        #if the user is adding an assignment
        if request.form.get("addDinosaurAssignment"):
            dinosaur = request.form["dinosaur"]
            employee = request.form["employee"]
            description = request.form["description"]
            if employee != "" or dinosaur != "" or description != "":
                emp = employee.split()
                fname = emp[0]
                lname = emp[1]
                query1 = "INSERT INTO Employees_To_Dinosaurs (e_id, d_id, description) \
                        VALUES ((SELECT id FROM Employees WHERE f_name = %s AND l_name = %s), \
                        (SELECT id FROM Dinosaurs WHERE name = %s),  (%s));"
                
                cur = mysql.connection.cursor()
                cur.execute(query1, (fname, lname, dinosaur, description))
                mysql.connection.commit()
        #redirect back to dinosaur assignments
        return redirect('/dinosaurAssignments')

    # get dinosaur assignments data
    if request.method == "GET":
        #SQL to get all the dinosaur assignments
        query2 = "SELECT  Employees_To_Dinosaurs.id AS id, \
            Dinosaurs.name AS 'Dinosaur', CONCAT(Employees.f_name, ' ', Employees.l_name) AS \
            'Employees Assigned', Employees_To_Dinosaurs.description AS 'Assignment' \
            FROM Employees_To_Dinosaurs INNER JOIN Dinosaurs ON Employees_To_Dinosaurs.d_id = \
            Dinosaurs.id INNER JOIN Employees ON Employees_To_Dinosaurs.e_id = Employees.id;"
        cur = mysql.connection.cursor()
        cur.execute(query2)

        dinosaur_assignment_data = cur.fetchall()

        #grab employee data for the drop down
        query3 = "SELECT CONCAT(f_name, ' ', l_name) AS employee FROM Employees"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        employee_data = cur.fetchall()

        # mySQL query to grab certification data for our dropdown
        query4 = "SELECT name FROM Dinosaurs;"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        dinosaur_data = cur.fetchall()

        #render the dinosaurAssignments and pass the nescasary data
        return render_template("dinosaurAssignments.j2", dinosaur_assignments=dinosaur_assignment_data,
         employees=employee_data, dinosaurs=dinosaur_data )


@app.route("/deleteAssignment/<int:id>", methods=["POST","GET"])
def deleteAssignment(id):
    if request.method == "GET":
        query1 = "SELECT  Employees_To_Dinosaurs.id AS id, \
        Dinosaurs.name AS 'Dinosaur', CONCAT(Employees.f_name, ' ', Employees.l_name) AS \
        'Employees Assigned', Employees_To_Dinosaurs.description AS 'Assignment' FROM Employees_To_Dinosaurs \
        INNER JOIN Dinosaurs ON Employees_To_Dinosaurs.d_id = Dinosaurs.id INNER JOIN Employees ON \
        Employees_To_Dinosaurs.e_id =Employees.id WHERE Employees_To_Dinosaurs.id = %s;"

        cur = mysql.connection.cursor()
        cur.execute(query1, (id,))
        data = cur.fetchall()

        return render_template("deleteAssignment.j2", data=data)

    if request.method == "POST":

        query = "DELETE FROM Employees_To_Dinosaurs WHERE Employees_To_Dinosaurs.id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to dinosaur page
    return redirect("/dinosaurAssignments")

@app.route('/updateAssignement/<int:id>', methods=["POST", "GET"])
def updateAssignment(id):
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab a specific dinosaur that the user selected
        query = "SELECT  Employees_To_Dinosaurs.id AS id, \
        Dinosaurs.name AS 'Dinosaur', CONCAT(Employees.f_name, ' ', Employees.l_name) AS \
        'Employees Assigned', Employees_To_Dinosaurs.description AS 'Assignment' FROM Employees_To_Dinosaurs \
        INNER JOIN Dinosaurs ON Employees_To_Dinosaurs.d_id = Dinosaurs.id INNER JOIN Employees ON \
        Employees_To_Dinosaurs.e_id =Employees.id WHERE Employees_To_Dinosaurs.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        # mySQL query to grab data for the location dropdown menu
        location_query = "SELECT name from Dinosaurs AS Dinosaur;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()

        # mySQL query to grab data for the species dropdown menu
        species_query = "SELECT CONCAT(f_name, ' ', l_name) AS 'Employee' FROM Employees;"
        cur = mysql.connection.cursor()
        cur.execute(species_query)
        spec_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("updateAssignment.j2", 
            data=data, locations=loc_data, 
            spec_data=spec_data)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("updateAssignment"):
            # grab user form inputs
            species = request.form["species"]
            location = request.form["location"]
            name = request.form["name"]
            status = request.form["status"]

        # TODO: account for null species
            if species == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, name, status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "UPDATE Dinosaurs\
                    SET species_id = (SELECT id FROM Species WHERE species_name=%s),\
                        location_id = (SELECT id FROM Locations WHERE location_name= %s),\
                        name = %s,\
                        health_status = %s\
                    WHERE id = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, name, status, id))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/dinosaurAssignments")



@app.route('/employees')
def employees():
    query = "SELECT * FROM Employees;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template("employees.j2", Species=results)


@app.route('/locations')
def locations():
    query = "SELECT * FROM Locations;"
    cur = mysql.connection.cursor()
    cur.execute(query)
    results = cur.fetchall()
    return render_template("locations.j2", Locations=results)




@app.route('/visitors', methods=["POST", "GET"])
def visitors():
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Visitors.id, Visitors.f_name, Visitors.l_name, Visitors.health_status, \
                Locations.location_name AS location \
                FROM Visitors \
                INNER JOIN Locations ON Locations.id = Visitors.location_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab data for dropdowns
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()


        

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("visitors.j2", data=data, locations=loc_data)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Visitor"):
            # grab user form inputs
            location = request.form["location"]
            f_name = request.form["f_name"]
            l_name = request.form["l_name"]
            status = request.form["status"]

        # TODO: account for null species
            if status == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (location,  status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "INSERT INTO Visitors(location_id, f_name, l_name, health_status) \
                VALUES((SELECT id FROM Locations WHERE location_name= %s), %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (location, f_name, l_name, status))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/visitors")

# route for delete functionality, deleting a visitor from Visitors
# we want to pass the 'id' value of that dinosaur on button click 
@app.route("/delete_visitor/<int:id>", methods=["POST", "GET"])
def delete_visitor(id):

    if request.method == "GET":
        # mysql query to gather the form's data
        query = "SELECT Visitors.id AS 'ID', Visitors.f_name AS 'f_name', Visitors.l_name AS 'l_name', Locations.location_name AS 'Location', Visitors.health_status AS 'Status'\
        FROM Visitors\
            INNER JOIN Locations ON Visitors.location_id = Locations.id WHERE Visitors.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("delete_visitor.j2", data=data)


    if request.method == "POST":
        query = "DELETE FROM Visitors WHERE Visitors.id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to dinosaur page
    return redirect("/visitors")

@app.route('/update_visitor/<int:id>', methods=["POST", "GET"])
def update_visitor(id):
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab a specific dinosaur that the user selected
        query =  query = "SELECT Visitors.id AS 'ID', Visitors.f_name AS 'f_name', Visitors.l_name AS \
            'l_name', Locations.location_name AS 'Location', Visitors.health_status AS 'Status'\
        FROM Visitors\
            INNER JOIN Locations ON Visitors.location_id = Locations.id WHERE Visitors.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()
       

        # mySQL query to grab data for the location dropdown menu
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()


        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("update_visitor.j2", 
            data=data, locations=loc_data, 
            status_options=status_options)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Update_Visitor"):
            # grab user form inputs
            location = request.form["location"]
            f_name = request.form["f_name"]
            l_name = request.form["l_name"]
            status = request.form["status"]

        # TODO: account for null species
            if species == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "UPDATE Visitors\
                    SET location_id = (SELECT id FROM Locations WHERE location_name= %s),\
                        f_name = %s,\
                        l_name = %s,\
                        health_status = %s\
                    WHERE id = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, ( location, f_name, l_name, status, id))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/visitors")



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1857)) 
    
    app.run(port=port, debug=True) 