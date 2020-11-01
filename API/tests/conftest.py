import os
import sys
import pika
import pytest
my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../source')

os.environ['MYSQL_HOST'] = 'localhost'
os.environ['MYSQL_USER'] = 'root'
os.environ['MYSQL_PASS'] = 'my-secret-pw'
os.environ['MYSQL_DATABASE'] = 'test'

os.environ['RABBITMQ_HOST'] = 'localhost'
os.environ['RABBITMQ_QUEUE'] = 'test'

from main import app
from database import db
from airport.model import Airport

from tests.fixtures import EXAMPLE_AIRPORT


@pytest.fixture
def api_client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def clean_airports():
    with app.app_context():
        db.session.execute("TRUNCATE TABLE airport")
        db.session.commit()
    yield
    with app.app_context():
        db.session.execute("TRUNCATE TABLE airport")
        db.session.commit()


@pytest.fixture
def one_airport_in_db():
    with app.app_context():
        db.session.execute("TRUNCATE TABLE airport")
        db.session.commit()
        temp_airport = Airport(**EXAMPLE_AIRPORT)
        db.session.add(temp_airport)
        db.session.commit()
    yield
    with app.app_context():
        db.session.execute("TRUNCATE TABLE airport")
        db.session.commit()


@pytest.fixture
def airport_model():
    with app.app_context():
        yield Airport


@pytest.fixture(scope="module")
def connect_rabbitmq():
    connection = pika.BlockingConnection()
    channel = connection.channel()
    channel.queue_delete(queue='test')
    yield channel
    channel.queue_delete(queue='test')
