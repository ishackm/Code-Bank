from flask import Flask, url_for,redirect, render_template,g
from flask import request
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData, Table
from sqlalchemy.pool import SingletonThreadPool



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/kinase_results', methods=['GET','POST'])
def kinase_results():

    engine=create_engine("sqlite:///final.db", poolclass=SingletonThreadPool)#,echo=True)
    Session=sessionmaker(bind=engine)
    session=Session()

    metadata = MetaData()
    alt_names=Table('Alt_names', metadata, autoload=True, autoload_with=engine)
    inhibitor=Table('Inhibitor',metadata,autoload=True,autoload_with=engine)
    kinase=Table('Kinase',metadata,autoload=True,autoload_with=engine)
    kinase_inhibitor=Table('Kinase_Inhibitor',metadata,autoload=True,autoload_with=engine)
    sub_phos=Table('Substrate_phosphosite',metadata,autoload=True,autoload_with=engine)
    substrate_kinase=Table('Substrate_site_Kinase',metadata,autoload=True,autoload_with=engine)
    substrate=Table('Substrate',metadata,autoload=True,autoload_with=engine)

    search = request.args.get('search')
    #search bar variable

    if len(search) > 0:
        #put search input into a seaprate variable . "search 1" linked in all queries
        #end result of search


        kdat=session.query(kinase).filter_by(Kinase_name=search).one()

        altdat=session.query(alt_names).filter_by(Kinase_name=search).all() #main bulk of data for page
        allnames=[]
        sbkid=[]
        for x in altdat:
            allnames.append(x.Protein_name) #gets all alt names for parsing through phosite and inhibitor
        for x in allnames:
            subkdat=session.query(substrate_kinase).filter_by(Kinase_name=x).all()
            for y in subkdat:
                if y.Substrate_kinase_ID not in sbkid:
                    sbkid.append(y.Substrate_kinase_ID)
        phositedat=[]
        for x in sbkid:
            phosite=session.query(sub_phos).filter_by(Substrate_kinase_ID=x).all()
            for y in phosite:
                phositedat.append(y[1:])
        ##
        inhibid=[]
        for x in allnames:
            kinhib=session.query(kinase_inhibitor).filter_by(Protein_name=x).all()
            for y in kinhib:
                inhibid.append(y.Inhibitor_ID)
        inhibdat=[]
        for x in inhibid:
            inhib=session.query(inhibitor).filter_by(Inhibitor_ID=x).one()
            inhibdat.append(inhib)

        inhibnames=[]
        for x in inhibdat:
            inhibnames.append(x[1])


        exampletuple=(kdat,phositedat,inhibdat)

        return render_template('kinase_result.html', exampletuple = exampletuple, kdat=kdat, phositedat=phositedat, inhibnames=inhibnames)

    elif len(search)==0:
        return render_template('input.html')
    else:
        return render_template('kinase_error.html')

@app.route('/kinase_search', methods=['GET','POST'])
def kinase_search():
    engine=create_engine("sqlite:///1.7 -funtional.db")#,echo=True)
    Session=sessionmaker(bind=engine)
    session=Session()
    from sqlalchemy import MetaData, Table
    metadata = MetaData()
    alt_names=Table('Alt_names', metadata, autoload=True, autoload_with=engine)
    inhibitor=Table('Inhibitor',metadata,autoload=True,autoload_with=engine)
    kinase=Table('Kinase',metadata,autoload=True,autoload_with=engine)
    kinase_inhibitor=Table('Kinase_Inhibitor',metadata,autoload=True,autoload_with=engine)
    sub_phos=Table('Substrate_phosphosite',metadata,autoload=True,autoload_with=engine)
    substrate_kinase=Table('Substrate_site_Kinase',metadata,autoload=True,autoload_with=engine)
    substrate=Table('Substrate',metadata,autoload=True,autoload_with=engine)
    #############
    search = request.args.get('search',type=str)
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
    return render_template('kinase-search-return-Richar.html',searchresult=searchresult)

@app.route('/inhibitor_search')
def inhibitor_search():
    return render_template('inhibitor_search.html')





@app.route('/inhibitor_result', methods=['GET','POST'])
def inhibitor_result():

    engine=create_engine("sqlite:///final.db", poolclass=SingletonThreadPool)#,echo=True)
    Session=sessionmaker(bind=engine)
    session=Session()

    metadata = MetaData()
    alt_names=Table('Alt_names', metadata, autoload=True, autoload_with=engine)
    inhibitor=Table('Inhibitor',metadata,autoload=True,autoload_with=engine)
    kinase=Table('Kinase',metadata,autoload=True,autoload_with=engine)
    kinase_inhibitor=Table('Kinase_Inhibitor',metadata,autoload=True,autoload_with=engine)
    sub_phos=Table('Substrate_phosphosite',metadata,autoload=True,autoload_with=engine)
    substrate_kinase=Table('Substrate_site_Kinase',metadata,autoload=True,autoload_with=engine)
    substrate=Table('Substrate',metadata,autoload=True,autoload_with=engine)
    search = request.args.get('search2')
    if len(search) > 0:
        inhibdat=session.query(inhibitor).filter_by(Inhibitor_name=search).first()
        kininhib=session.query(kinase_inhibitor).filter_by(Inhibitor_ID=inhibdat.Inhibitor_ID).all()
        inhibidata=inhibdat[1:]
        kininhibl=[]
        for x in kininhib:
            kininhibl.append(x[2])

        return render_template('inhibitor_result.html', kininhibl = kininhibl, inhibidata=inhibidata,kininhib=kininhib)

    elif len(search)==0:
        return render_template('input.html')

    else:
            return render_template('kinase_error.html')







def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


ALLOWED_EXTENSIONS = {'tsv'}

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
            #process_file('fold_change.png', file )
            return redirect(url_for('result'))
            return render_template('upload.html')



@app.route('/upload')
def upload(): # Upload page URL route
    return render_template('upload.html')

@app.route('/upload2')
def upload2(): # Upload page 2 URL route
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

@app.route('/kinase_error')
def kinase_error(): # Kinase Error route
    return render_template('kinase_error.html')

@app.route('/input')
def input(): # No Input URL route
    return render_template('input.html')


@app.errorhandler(404)
def error_404(error): # 404 Error page URL route
        return render_template('error.html'), 404

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
