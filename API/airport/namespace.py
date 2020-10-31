import io
import csv

from werkzeug.datastructures import FileStorage
from flask_restx import Namespace, Resource

from database import db
from airport.model import Airport, airport_api_model

api = Namespace('airports', description='Airports API')

airport = api.model('Airport', airport_api_model)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)


@api.route('/')
class AirportCR(Resource):

    @api.doc('list_airports')
    @api.marshal_list_with(airport)
    def get(self):
        return Airport.query.all()

    @api.doc('create_airport')
    @api.expect(airport)
    @api.marshal_with(airport, code=201)
    def post(self):
        temp_airport = Airport(**api.payload)
        db.session.add(temp_airport)
        db.session.commit()
        return temp_airport, 201


@api.route('/<id>')
class AirportUD(Resource):

    @api.doc('delete_airport')
    def delete(self, id):
        Airport.query.filter_by(id=id).delete()
        db.session.commit()
        return 204

    @api.doc('update_airport')
    @api.expect(airport)
    @api.marshal_with(airport, code=200)
    def put(self, id):
        n_updated = Airport.query.filter_by(id=id).update(api.payload)
        db.session.commit()
        temp_airport = Airport.query.filter_by(id=id).first()
        return temp_airport, 200


@api.route('/csv')
class AirportUD(Resource):

    @api.expect(upload_parser)
    @api.doc('update_airport_by_csv')
    def post(self):
        file = io.StringIO(upload_parser.parse_args().file.stream.read().decode())
        csv_reader = csv.reader(file, delimiter=',')
        headers = next(csv_reader)
        headers = [x.lower() for x in headers]
        for row in csv_reader:
            line = [x if x != '' else None for x in row]
            element = dict(zip(headers, line))
            temp_airport = Airport(**element)
            db.session.add(temp_airport)
            db.session.flush()
        db.session.commit()
        return 200
