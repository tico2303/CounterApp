from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")
Bootstrap(app)
db = SQLAlchemy(app)

#from views import *

if __name__ == '__main__':
        app.run(debug=True)
