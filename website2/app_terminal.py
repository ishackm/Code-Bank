from flask import Flask, url_for,redirect, render_template,g
from flask import request
#from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
from uploadfinal import process_file
import os
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy
import sqlite3


app = Flask(__name__) # Start the Flask app

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'csv'}

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        if 'file' not in request.files:
            print('Please upload a csv file')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            #filename = secure_filename(file)
            process_file('fold_change.png', file )
            return redirect(url_for('result'))
            return render_template('upload.html')



app.config['SECRET_KEY'] = 'change this unsecure key'


# create a class to define the form
class KinaseForm(FlaskForm): # WT Form kinase form name
	kinase_name = StringField('', validators=[Required()]) # search field for the kinase name
	submit = SubmitField('Submit') # submit button


def connect_db(path):
    return sqlite3.connect(path) # connect to the Database

@app.before_request
def before_request():
    g.db_connection=connect_db("final.db")

def query_db(query,args=()):
    cursor = g.db_connection.execute(query, args) # execute the user queryreturn cursor
    return cursor


@app.route('/', methods = ['GET', 'POST'])
def index():
    kinase_form=KinaseForm() # kinase form
    kinase_name= None
    if kinase_form.validate_on_submit(): # if kinase name is on db
        kinase_name=kinase_form.kinase_name.data
        print ('\n\n\n'+ kinase_name +'\n\n\n')
        return redirect(url_for('kinase_BG',kinase_name=kinase_name))
    return render_template('index.html', form=kinase_form,kinase_name=kinase_name)

#@app.route('/<kinase_name>')
#def kinase_BG(kinase_name):
    #kinase_name=kinase_name.upper()
    #BG= query_db("SELECT * FROM Kinase WHERE Kinase.Kinase_name=?", (kinase_name,))
    #kinases = [dict(Kinase_name=row[0],Accession_number=row[1],Gene_symbol=row[2],Gene_family=row[3],Cell_location=row[4],Genome_location=row[5],Protein_longname=row[6]) for row in BG.fetchall()]

    #target= query_db("SELECT DISTINCT Substrate_name FROM Substrate_phosphosite INNER JOIN kinase ON kinase.name = Substrate_site_kinase ON Substrate_site_kinase = kinase WHERE kinase.name?",(kinase_name,))
    #return render_template ("sql.html", kinases=kinases,kinase_name=kinase_name)


@app.route('/upload')
def upload(): # Upload page URL route
    return render_template('upload.html')

@app.route('/upload2')
def upload2(): # Upload_2 page URL route
    return render_template('upload_page2.html')

@app.route('/kinase_db')
def kinase_db(): # Kinase Database page URL route
    return render_template('kinase_db.html')

@app.route('/inhibitor_db')
def inhibitor_db():# Kinase Inhibitor page URL route
    return render_template('inhibitor_db.html')

@app.route('/result')
def result(): # Result URL route
    return render_template('result.html')

@app.errorhandler(404)
def error_404(error): # 404 Error page URL route
        return render_template('error.html'), 404

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
