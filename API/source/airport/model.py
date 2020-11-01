from flask_restx import fields

from database import db


class Airport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(256), nullable=False)
    country = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text)
    iata = db.Column(db.String(8))
    icao = db.Column(db.String(8))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    altitude = db.Column(db.Integer, nullable=False)
    timezone = db.Column(db.Integer)
    dst = db.Column(db.String(8))
    tz = db.Column(db.String(64))
    type = db.Column(db.String(64), nullable=False)
    source = db.Column(db.String(64), nullable=False)


airport_api_model = {
    'id': fields.Integer(readonly=True, description='The Airport unique identifier'),
    'name': fields.String(required=True, description='The Airport name'),
    'country': fields.String(required=True, description='The Airport country'),
    'city': fields.String(required=False, description='The Airport city'),
    'iata': fields.String(required=False, description='The Airport iata'),
    'icao': fields.String(required=True, description='The Airport icao'),
    'latitude': fields.Float(required=True, description='The Airport latitude'),
    'longitude': fields.Float(required=True, description='The Airport longitude'),
    'altitude': fields.Integer(required=True, description='The Airport altitude'),
    'timezone': fields.Integer(required=False, description='The Airport timezone'),
    'dst': fields.String(required=True, description='The Airport dst'),
    'tz': fields.String(required=True, description='The Airport timezone code'),
    'type': fields.String(required=True, description='The Airport type'),
    'source': fields.String(required=True, description='The Airport source')
}
