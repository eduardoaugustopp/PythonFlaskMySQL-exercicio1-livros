import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

SECRET_KEY = 'eduardo'

SQLALCHEMY_DATABASE_URI = \
    '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD='mysql+mysqlconnector',
        usuario='root',
        senha='admin123',
        servidor='localhost',
        database='livraria'
    )

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

from views_game import *
from views_user import *

if __name__ == '__main__':
    app.run(debug=True)
