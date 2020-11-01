import os
import pymysql
from flask import Flask
from flask_restx import Api

from database import db
from airport.namespace import api as airports

pymysql.install_as_MySQLdb()

app = Flask(__name__)
api = Api(app, version='1.0', title='Passnfly Test')

mysql_uri = f"mysql://{os.getenv('MYSQL_USER')}:" \
            f"{os.getenv('MYSQL_PASS')}@" \
            f"{os.getenv('MYSQL_HOST')}:3306/" \
            f"{os.getenv('MYSQL_DATABASE')}"
app.config["SQLALCHEMY_DATABASE_URI"] = mysql_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db.init_app(app)
api.add_namespace(airports)
db.create_all(app=app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
