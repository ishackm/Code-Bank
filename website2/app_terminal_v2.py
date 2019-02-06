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

from db import app
from db_setup import init_db, db_session
from form import KinaseForm
from flask import flash, render_template, request, redirect
from models import Alt_names
from tables import Results

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    search = KinaseForm(request.form)
    if request.method == 'POST':
        return search_results(search)

    return render_template('index.html', form=search)

@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db_session.query(Alt_names)
        results = qry.all()

    if not results:
        return redirect(404)
    else:
        # display results
        table = Results(results)
        table.border = True
        return render_template('results.html', table=table)




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
