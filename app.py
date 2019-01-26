from flask import Flask, url_for,redirect, render_template
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, View, Link, Text, Separator

app = Flask(__name__)
nav = Nav(app)

nav.register_element('my_navbar', Navbar(
'thenav',
View('Home ', 'index')))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')




if __name__ == '__main__':
    app.run(debug=True)
