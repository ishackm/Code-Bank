from flask import Flask, url_for,redirect, render_template,g
from flask import request
from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, configure_uploads, DATA
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy



application= app = Flask(__name__)

@app.route('/')
def index():  # Homepage URL route
    return render_template('index.html')


# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
