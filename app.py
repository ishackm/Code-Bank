from flask import Flask, url_for,redirect, render_template
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
from uploadfinal import uploaded_file



app = Flask(__name__) # Start the Flask app


@app.route('/')
def index(): # Home page URL route
    return render_template('index.html')

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

@app.route('/sql')
def sql(): # SQLite Database URL route
    return render_template('sql.html')

@app.errorhandler(404)
def error_404(error): # 404 Error page URL route
        return render_template('error.html'), 404

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
