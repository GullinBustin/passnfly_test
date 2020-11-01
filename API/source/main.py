import os
import pymysql
from flask import Flask
from flask_restx import Api

from database import db
from airport.namespace import api as airports

pymysql.install_as_MySQLdb()

app = Flask(__name__)
api = Api(app, version='1.0', title='Passnfly Test')
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('MYSQL_URI')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)
api.add_namespace(airports)
db.create_all(app=app)

if __name__ == '__main__':
    app.run(debug=True)
