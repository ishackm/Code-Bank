from flask import Flask, url_for,redirect, render_template,g
from flask import request
#from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
from uploadfinal import process_file
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from db import session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kinase_results', methods=['GET','POST'])
def kinase_results(search):
    search1="%"+search+"%"
    searchresult=[]
    likequery=session.query(kinase).filter(kinase.c.Kinase_name.like(search1)).all()
    if likequery!=[]: #if search found kinases, aka if the search entry was a kinase name
        for x in likequery:
            if x not in searchresult:
                searchresult.append(x[:3])
    likequery=session.query(kinase).filter(kinase.c.Accession_number.like(search1)).all()
    if likequery!=[]: #if search was an accession number or like an accession number
        for x in likequery:
            if x not in searchresult:
                searchresult.append(x[:3])
    likequery=session.query(kinase).filter(kinase.c.Gene_symbol.like(search1)).all()
    if likequery!=[]: #if search was a gene symbol or like a gene symbol
        for x in likequery:
            if x not in searchresult:
                searchresult.append(x[:3])

    likequery=session.query(alt_names).filter(alt_names.c.Protein_name.like(search1)).all()
    if likequery!=[]:
        k_alts=[]
        for x in likequery:
            if x.Kinase_name not in k_alts:
                k_alts.append(x.Kinase_name)
        for x in k_alts:
            likequery=session.query(kinase).filter(kinase.c.Kinase_name.like(x)).all()
            if likequery!=[]: #if search found kinases, aka if the search entry was a kinase name
                for x in likequery:
                    if x not in searchresult:
                        searchresult.append(x[:3])
            result= new_function(query)
    elif not request.args.get('search'):
        return "Invalid Kinase Name, Please check again"
    else:
        print ('Query was:',query)
        return render_template('kinase_result.html')






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
