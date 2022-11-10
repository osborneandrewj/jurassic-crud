from flask import Flask, render_template, json
import os
import database.db_connector as db

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/dinosaurs')
def dinosaurs():
    # Write the query and save it to a variable
    query = "SELECT * FROM Dinosaurs;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    # return results
    return render_template("dinosaurs.j2", Dinosaurs=results)


@app.route('/species')
def species():
    # Write the query and save it to a variable
    query = "SELECT * FROM Species;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    # return results
    return render_template("species.j2", Species=results)


@app.route('/dinosaurAssignments')
def dinosaurAssignments():
    # Write the query and save it to a variable
    query = "SELECT * FROM Employees_To_Dinosaurs;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    # return results
    return render_template("dinosaurAssignments.j2", dinosaurAssignments=results)

@app.route('/employees')
def employees():
    # Write the query and save it to a variable
    query = "SELECT * FROM Employees;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    # return results
    return render_template("employees.j2", Species=results)


@app.route('/locations')
def locations():
    # Write the query and save it to a variable
    query = "SELECT * FROM Locations;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    # return results
    return render_template("locations.j2", Locations=results)


@app.route('/visitors')
def visitors():
    # Write the query and save it to a variable
    query = "SELECT * FROM Visitors;"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    results = cursor.fetchall()

    # Sends the results back to the web browser.
    # return results
    return render_template("visitors.j2", Visitors=results)
# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1857)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 