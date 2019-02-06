from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, DATA

app = Flask(__name__)

def uploaded_file():
    photos = UploadSet('photos', DATA)
    app.config['UPLOADED_PHOTOS_DEST'] = 'static/csv'
    configure_uploads(app, photos)

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
        return render_template('upload.html')
