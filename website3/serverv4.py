from flask import Flask, url_for,redirect, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')




if __name__ == '__main__':
    app.run(debug=True)
