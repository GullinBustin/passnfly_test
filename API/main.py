import pymysql
from flask import Flask
from flask_restx import Api

from database import db
from airport.namespace import api as airports

pymysql.install_as_MySQLdb()

app = Flask(__name__)
api = Api(app, version='1.0', title='Passnfly Test')
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:my-secret-pw@127.0.0.1:3306/test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)
api.add_namespace(airports)

if __name__ == '__main__':
    db.create_all(app=app)
    app.run(debug=True)
