from flask import Flask, url_for,redirect, render_template, request
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator
from flask_uploads import UploadSet, configure_uploads, DATA


app = Flask(__name__)
nav = Nav(app)

nav.register_element('my_navbar', Navbar(
'thenav',
View('Home ', 'index')))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    photos = UploadSet('photos', DATA)
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/csv'
    configure_uploads(app, photos)

    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
        return render_template('upload.html')

@app.route('/kinase_db')
def kinase_db():
    return render_template('kinase_db.html')

@app.route('/inhibitor_db')
def inhibitor_db():
    return render_template('inhibitor_db.html')

@app.errorhandler(404)
def error_404(error):
        return render_template('error.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
