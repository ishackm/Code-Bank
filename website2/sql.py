import sqlite3
from flask import Flask, g, render_template

app = Flask(__name__)

def connect_db(path):
    return sqlite3.connect(path)

@app.before_request
def before_request():
    g.db_connection = connect_db("final.db")

def query_db(query,args=()):
    cursor = g.db_connection.execute(query, args)
    return cursor

@app.route('/<kinase_name>')
def main (kinase_name):
    cursor = query_db("SELECT Kinase.Kinase_name FROM Kinase WHERE Kinase_name=?", (kinase_name,))
    targets= [dict(Gene_family=row[0]) for row in cursor.fetchall()]
    return render_template ('sql_v2.html', targets=targets)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
