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

# Data used to pre-populate dropdown menu options
status_options = ["healthy", "sick", "injured", "deceased", "eaten"]
diet_options = ["carnivore", "omnivore", "herbivore"]
electric_status_options = ["online", "reserve", "offline"]
security_status_options = ["online", "lockdown", "offline"]

# Routes 

@app.route('/')
def root():
    return redirect("/dinosaurs")

@app.route('/dinosaurs', methods=["POST", "GET"])
def dinosaurs():
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Dinosaurs.id AS 'ID', Dinosaurs.name AS 'Name', Species.species_name AS 'Species', Locations.location_name AS 'Location', Dinosaurs.health_status AS 'Status'\
            FROM Dinosaurs\
            INNER JOIN Species ON Dinosaurs.species_id = Species.id\
            LEFT OUTER JOIN Locations ON Dinosaurs.location_id = Locations.id;"
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
                LEFT OUTER JOIN Locations ON Dinosaurs.location_id = Locations.id WHERE Dinosaurs.id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        # mySQL query to grab data for the location dropdown menu
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()
        print("loc_data: " + str(loc_data))

        # mySQL query to grab data for the species dropdown menu
        species_query = "SELECT species_name from Species;"
        cur = mysql.connection.cursor()
        cur.execute(species_query)
        spec_data = cur.fetchall()

        return render_template("update_dinosaur.j2", 
            data=data, locations=loc_data, 
            spec_data=spec_data, status_options=status_options)

    if request.method == "POST":
        # fire off if user presses the Update Dinosaur button
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
            LEFT OUTER JOIN Locations ON Dinosaurs.location_id = Locations.id WHERE Dinosaurs.id = %s"
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

@app.route('/species', methods=["POST", "GET"])
def species():
    # Grab species data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the Species
        query = "SELECT Species.id AS 'ID', Species.species_name AS 'Species Name', Species.diet AS 'Diet' FROM Species;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("/species/species.j2", data=data, diet_options=diet_options)

    if request.method == "POST":
        # fire off if user presses the Add Species button
        if request.form.get("Add_Species"):
            # grab user form inputs
            name = request.form["name"]
            diet = request.form["diet"]

            query = "INSERT INTO Species(species_name, diet)\
                VALUES(%s, %s);"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, diet))
            mysql.connection.commit()

        return redirect("/species")

@app.route('/update_species/<int:id>', methods=["POST", "GET"])
def update_species(id):
    # Grab Species data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab the specific species that the user selected
        query = "SELECT Species.id AS 'ID', Species.species_name AS 'Species', Species.diet AS 'Diet'\
            FROM Species\
            WHERE Species.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("species/update_species.j2", 
            data=data, diet_options=diet_options)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Update_Species"):
            # grab user form inputs
            name = request.form["name"]
            diet = request.form["diet"]

            query = "UPDATE Species\
                SET species_name = %s,\
                    diet = %s\
                WHERE Species.id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, diet, id))
            mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/species")

# route for delete functionality, deleting a species from Species,
# we want to pass the 'id' value of that species on button click 
@app.route("/delete_species/<int:id>", methods=["POST", "GET"])
def delete_species(id):

    if request.method == "GET":
        # mysql query to gather the form's data
        query = "SELECT Species.id AS 'ID', Species.species_name AS 'Species Name', Species.diet AS 'Diet' FROM Species\
            WHERE Species.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("/species/delete_species.j2", data=data)


    if request.method == "POST":
        query = "DELETE FROM Species WHERE Species.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to Species page
    return redirect("/species")


@app.route('/dinosaurAssignments', methods=["POST", "GET"])
def dinosaurAssignments():
    #insert a dino assignment into the table
    if request.method == 'POST':
        #if the user is adding an assignment
        if request.form.get("Add_Assignment"):
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
                
                data = mysql.connection.cursor()
                data.execute(query1, (fname, lname, dinosaur, description))
                mysql.connection.commit()
        #redirect back to dinosaur assignments
        return redirect('/dinosaurAssignments')

    # get dinosaur assignments data
    if request.method == "GET":
        #SQL to get all the dinosaur assignments
        query2 = "SELECT  Employees_To_Dinosaurs.id AS ID, \
            Dinosaurs.name AS 'Dinosaur', CONCAT(Employees.f_name, ' ', Employees.l_name) AS \
            'Employees Assigned', Employees_To_Dinosaurs.description AS 'Assignment' \
            FROM Employees_To_Dinosaurs INNER JOIN Dinosaurs ON Employees_To_Dinosaurs.d_id = \
            Dinosaurs.id INNER JOIN Employees ON Employees_To_Dinosaurs.e_id = Employees.id;"
        cur = mysql.connection.cursor()
        cur.execute(query2)

        data = cur.fetchall()

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
        return render_template("dinosaurAssignments.j2", data=data,
         employees=employee_data, dinosaurs=dinosaur_data )


@app.route("/delete_assignment/<int:id>", methods=["POST","GET"])
def deleteAssignment(id):
    if request.method == "GET":
        query1 = "SELECT  Employees_To_Dinosaurs.id AS ID, \
        Dinosaurs.name AS 'Dinosaur', CONCAT(Employees.f_name, ' ', Employees.l_name) AS \
        'Employees Assigned', Employees_To_Dinosaurs.description AS 'Assignment' FROM Employees_To_Dinosaurs \
        INNER JOIN Dinosaurs ON Employees_To_Dinosaurs.d_id = Dinosaurs.id INNER JOIN Employees ON \
        Employees_To_Dinosaurs.e_id =Employees.id WHERE Employees_To_Dinosaurs.id = %s;"

        cur = mysql.connection.cursor()
        cur.execute(query1, (id,))
        data = cur.fetchall()

        return render_template("delete_assignment.j2", data=data)

    if request.method == "POST":

        query = "DELETE FROM Employees_To_Dinosaurs WHERE Employees_To_Dinosaurs.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to dinosaur page
    return redirect("/dinosaurAssignments")

@app.route('/update_assignment/<int:id>', methods=["POST", "GET"])
def updateAssignment(id):
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab a specific dinosaur that the user selected
        query = "SELECT  Employees_To_Dinosaurs.id AS ID, \
        Dinosaurs.name AS 'Dinosaur', CONCAT(Employees.f_name, ' ', Employees.l_name) AS \
        'Employee', Employees_To_Dinosaurs.description AS 'Assignment' FROM Employees_To_Dinosaurs \
        INNER JOIN Dinosaurs ON Employees_To_Dinosaurs.d_id = Dinosaurs.id INNER JOIN Employees ON \
        Employees_To_Dinosaurs.e_id =Employees.id WHERE Employees_To_Dinosaurs.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        # mySQL query to grab data for the Dinosaur dropdown menu
        dino_query = "SELECT name from Dinosaurs;"
        cur = mysql.connection.cursor()
        cur.execute(dino_query)
        dino_data = cur.fetchall()

        # mySQL query to grab data for the species dropdown menu
        emp_query = "SELECT CONCAT(f_name, ' ', l_name) AS 'Employee' FROM Employees;"
        cur = mysql.connection.cursor()
        cur.execute(emp_query)
        emp_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("update_assignment.j2", 
            data=data, dinosaurs=dino_data, 
            employees=emp_data)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Update_Assignment"):
            # grab user form inputs
            dinosaur = request.form["dinosaur"]
            employee = request.form["employee"]
            description = request.form["description"]
           
            emp = employee.split()
            fname = emp[0]
            lname = emp[1]


            query = "UPDATE Employees_To_Dinosaurs\
                    SET e_id = (SELECT id FROM Employees WHERE Employees.f_name = %s AND\
                        Employees.l_name = %s),\
                        d_id = (SELECT id from Dinosaurs where Dinosaurs.name =%s),\
                        description = %s\
                    WHERE id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (fname, lname, dinosaur, description, id))
            mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/dinosaurAssignments")



@app.route('/employees', methods=["GET", "POST"])
def employees():
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Employees.id AS 'ID', Employees.f_name AS 'First Name', \
                Employees.l_name AS 'Last Name', Employees.job_title AS 'Job Title', \
                Employees.salary AS 'Salary', Employees.health_status AS 'Health Status', \
                Locations.location_name AS Location \
                FROM Employees \
                LEFT OUTER JOIN Locations ON Locations.id = Employees.location_id;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab data for dropdowns
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()

        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("employees.j2", data=data, locations=loc_data)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Add_Employee"):
            # grab user form inputs
            location = request.form["location"]
            f_name = request.form["f_name"]
            l_name = request.form["l_name"]
            job_title = request.form["job_title"]
            salary = request.form["salary"]
            status = request.form["status"]

        # TODO: account for null species
            if status == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (location,  status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "INSERT INTO Employees(location_id, f_name, l_name, job_title, salary, health_status) \
                VALUES((SELECT id FROM Locations WHERE location_name= %s), %s, %s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(query, (location, f_name, l_name, job_title, salary, status))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/employees")

# route for delete functionality, deleting a visitor from Visitors
# we want to pass the 'id' value of that dinosaur on button click 
@app.route("/delete_employee/<int:id>", methods=["POST", "GET"])
def delete_employee(id):

    if request.method == "GET":
        # mysql query to gather the form's data
        query = "SELECT Employees.id AS 'ID', Employees.f_name AS 'f_name', Employees.l_name AS 'l_name', \
                Employees.job_title AS 'job_title', Employees.salary AS 'salary', Locations.location_name \
                AS 'Location', Employees.health_status AS 'Status'\
            FROM Employees\
            LEFT OUTER JOIN Locations ON Employees.location_id = Locations.id WHERE Employees.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("delete_employee.j2", data=data)


    if request.method == "POST":
        query = "DELETE FROM Employees WHERE Employees.id = '%s';"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to dinosaur page
    return redirect("/employees")

@app.route('/update_employee/<int:id>', methods=["POST", "GET"])
def update_employee(id):
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab a specific dinosaur that the user selected
        query =  "SELECT Employees.id AS 'ID', Employees.f_name AS 'f_name', Employees.l_name AS 'l_name', \
                Employees.job_title AS 'job_title', Employees.salary AS 'salary', Locations.location_name \
                AS 'Location', Employees.health_status AS 'Status'\
            FROM Employees\
            LEFT OUTER JOIN Locations ON Employees.location_id = Locations.id WHERE Employees.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()
       

        # mySQL query to grab data for the location dropdown menu
        location_query = "SELECT location_name from Locations;"
        cur = mysql.connection.cursor()
        cur.execute(location_query)
        loc_data = cur.fetchall()


        # render edit_people page passing our query data and homeworld data to the edit_people template
        return render_template("update_employee.j2", 
            data=data, locations=loc_data, 
            status_options=status_options)

    if request.method == "POST":
        # fire off if user presses the Add Person button
        if request.form.get("Update_Employee"):
            # grab user form inputs
            location = request.form["location"]
            f_name = request.form["f_name"]
            l_name = request.form["l_name"]
            job_title = request.form["job_title"]
            salary = request.form["salary"]
            status = request.form["status"]

        # TODO: account for null species
            if species == "":
                query = ""
                cur = mysql.connection.cursor()
                cur.execute(query, (species, location, status))
                mysql.connection.commit()

        # no null inputs
            else:
                query = "UPDATE Employees\
                    SET location_id = (SELECT id FROM Locations WHERE location_name= %s),\
                        f_name = %s,\
                        l_name = %s,\
                        job_title = %s, \
                        salary = %s, \
                        health_status = %s\
                    WHERE id = %s;"
                cur = mysql.connection.cursor()
                cur.execute(query, ( location, f_name, l_name, job_title, salary, status, id))
                mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/employees")


@app.route('/locations', methods=["POST", "GET"])
def locations():

    if request.method == "GET":

        # mySQL query to grab data for the species dropdown menu
        species_query = "SELECT species_name from Species;"
        cur = mysql.connection.cursor()
        cur.execute(species_query)
        species_list = cur.fetchall()

        # mySQL query to grab permitted species data
        permitted_species_query = "SELECT Locations.id, Species.species_name\
            FROM Locations\
            INNER JOIN Species_Allowed_Locations ON Locations.id = Species_Allowed_Locations.l_id\
            INNER JOIN Species ON Species_Allowed_Locations.s_id = Species.id;"
        cur = mysql.connection.cursor()
        cur.execute(permitted_species_query)
        permitted_species = cur.fetchall()

        query = "SELECT Locations.id AS 'ID',\
            Locations.location_name AS 'Name',\
            Locations.electric_grid_status AS 'Electricity',\
            Locations.security_status AS 'Security'\
            FROM Locations;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("/locations/locations.j2", data=data, species_list=species_list, permitted_species=permitted_species,
            security_status_options=security_status_options, 
            electric_status_options=electric_status_options)

    if request.method == "POST":
        # fire off if user presses the Add Location button
        if request.form.get("Add_Location"):
            # grab user form inputs
            name = request.form["name"]
            electrical = request.form["electrical"]
            security = request.form["security"]
            print(name, electrical, security)

        query = "INSERT INTO Locations(location_name, electric_grid_status, security_status)\
            VALUES(%s, %s, %s);"
        print(query)
        cur = mysql.connection.cursor()
        cur.execute(query, (name, electrical, security))
        mysql.connection.commit()

        return redirect("/locations")

@app.route("/delete_location/<int:id>", methods=["POST", "GET"])
def delete_location(id):

    if request.method == "GET":
        # mySQL query to grab permitted species data
        permitted_species_query = "SELECT Locations.id, Species.species_name\
            FROM Locations\
            INNER JOIN Species_Allowed_Locations ON Locations.id = Species_Allowed_Locations.l_id\
            INNER JOIN Species ON Species_Allowed_Locations.s_id = Species.id;"
        cur = mysql.connection.cursor()
        cur.execute(permitted_species_query)
        permitted_species = cur.fetchall()

        query = "SELECT Locations.id AS 'ID',\
            Locations.location_name AS 'Name',\
            Locations.electric_grid_status AS 'Electricity',\
            Locations.security_status AS 'Security'\
            FROM Locations\
            WHERE Locations.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("/locations/delete_location.j2", data=data, permitted_species=permitted_species)


    if request.method == "POST":
        query = "DELETE FROM Locations WHERE Locations.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        mysql.connection.commit()

    # redirect back to Species page
    return redirect("/locations")


@app.route('/update_location/<int:id>', methods=["POST", "GET"])
def update_location(id):
    # Grab Species data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab data for the species list menu
        species_query = "SELECT species_name, id from Species;"
        cur = mysql.connection.cursor()
        cur.execute(species_query)
        species_list = cur.fetchall()

        # mySQL query to grab permitted species data
        permitted_species_query = "SELECT Locations.id, Species.species_name, Species.id AS s_id\
            FROM Locations\
            INNER JOIN Species_Allowed_Locations ON Locations.id = Species_Allowed_Locations.l_id\
            INNER JOIN Species ON Species_Allowed_Locations.s_id = Species.id\
            WHERE Locations.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(permitted_species_query, (id,))
        permitted_species = cur.fetchall()
        permitted_species_ids = []
        for item in permitted_species:
            permitted_species_ids.append(item["s_id"])

        query = "SELECT Locations.id AS 'ID',\
            Locations.location_name AS 'Name',\
            Locations.electric_grid_status AS 'Electricity',\
            Locations.security_status AS 'Security'\
            FROM Locations\
            WHERE Locations.id = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (id,))
        data = cur.fetchall()

        return render_template("locations/update_location.j2", 
            data=data, permitted_species=permitted_species, permitted_species_ids=permitted_species_ids, 
            security_status_options=security_status_options, 
            electric_status_options=electric_status_options, species_list=species_list)

    if request.method == "POST":
        # fire off if user presses the edit location button
        if request.form.get("Update_Location"):
            # grab user form inputs
            name = request.form["name"]
            electrical = request.form["electrical"]
            security = request.form["security"]
            user_selected_species = request.form.getlist("allow_species")

            # mySQL query to grab permitted species data
            permitted_species_query = "SELECT Locations.id, Species.species_name, Species.id AS s_id\
                FROM Locations\
                INNER JOIN Species_Allowed_Locations ON Locations.id = Species_Allowed_Locations.l_id\
                INNER JOIN Species ON Species_Allowed_Locations.s_id = Species.id\
                WHERE Locations.id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(permitted_species_query, (id,))
            permitted_species = cur.fetchall()
            permitted_species_ids = []
            for item in permitted_species:
                permitted_species_ids.append(item["s_id"])

            duplicate_list = []
            # delete all intermediary species tables not in user selection
            for s_id in permitted_species_ids:
                if s_id not in user_selected_species:
                    duplicate_list.append(s_id)
                    query = "DELETE from Species_Allowed_Locations\
                        WHERE Species_Allowed_Locations.l_id = %s\
                        AND Species_Allowed_Locations.s_id = %s;"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (id, s_id))
                    mysql.connection.commit()

            # then iterate through the list of user species selections and add any additional tables
            for item in user_selected_species:
                if item not in duplicate_list:
                    query = "INSERT INTO Species_Allowed_Locations(s_id, l_id)\
                        VALUES(%s, %s);"
                    cur = mysql.connection.cursor()
                    cur.execute(query, (item, id))
                    mysql.connection.commit()  

            query = "UPDATE Locations\
                SET location_name = %s,\
                    electric_grid_status = %s,\
                    security_status = %s\
                WHERE Locations.id = %s;"
            cur = mysql.connection.cursor()
            cur.execute(query, (name, electrical, security, id))
            mysql.connection.commit()

        # redirect back to Dinosaurs page
        return redirect("/locations")



@app.route('/visitors', methods=["POST", "GET"])
def visitors():
    # Grab Dinosaurs data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in bsg_people
        query = "SELECT Visitors.id AS 'ID', Visitors.f_name AS 'First Name', \
                Visitors.l_name AS 'Last Name', Visitors.health_status AS 'Health Status', \
                Locations.location_name AS 'Location' \
                FROM Visitors \
                LEFT OUTER JOIN Locations ON Locations.id = Visitors.location_id;"
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
            LEFT OUTER JOIN Locations ON Visitors.location_id = Locations.id WHERE Visitors.id = %s;"
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