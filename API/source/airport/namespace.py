import io
import os
import csv
import json
import pika

from werkzeug.datastructures import FileStorage
from flask_restx import Namespace, Resource

from database import db
from airport.model import Airport, airport_api_model

api = Namespace('airports', description='Airports API')

airport = api.model('Airport', airport_api_model)

upload_parser = api.parser()
upload_parser.add_argument('file', location='files',
                           type=FileStorage, required=True)

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_queue = os.getenv('RABBITMQ_QUEUE')


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
@api.doc(params={'id': 'Airport ID'})
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
class AirportCSV(Resource):

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
        return


def job_body_builder(method, id=None, params=None):
    if not params:
        params = {}
    return json.dumps({"method": method, "params": params, "id": id})


@api.route('/add-job')
class AirportJobC(Resource):

    @api.doc('job_create_airport')
    @api.expect(airport)
    def post(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=rabbitmq_queue,
            body=job_body_builder("create", params=api.payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
        return 200


@api.route('/add-job/<id>')
@api.doc(params={'id': 'Airport ID'})
class AirportJobUD(Resource):

    @api.doc('job_delete_airport')
    def delete(self, id):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=rabbitmq_queue,
            body=job_body_builder("delete", id=id),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
        return 200

    @api.doc('job_update_airport')
    @api.expect(airport)
    def put(self, id):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        channel.queue_declare(queue=rabbitmq_queue, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=rabbitmq_queue,
            body=job_body_builder("update", id=id, params=api.payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ))
        connection.close()
        return 200

#TODO Responses