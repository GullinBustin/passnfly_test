import json
import pytest

from tests.fixtures import EXAMPLE_AIRPORT, CSV_AIRPORTS


def test_add_airport_async(api_client, connect_rabbitmq):
    response = api_client.post("/airports/add-job", json=EXAMPLE_AIRPORT)
    method_frame, header_frame, body = connect_rabbitmq.basic_get('test')
    connect_rabbitmq.basic_ack(method_frame.delivery_tag)
    body_json = json.loads(body)
    assert body_json["method"] == "create"
    assert body_json["params"] == EXAMPLE_AIRPORT


@pytest.mark.usefixtures("one_airport_in_db")
def test_delete_airport_async(api_client, connect_rabbitmq):
    response = api_client.delete("/airports/add-job/1")
    method_frame, header_frame, body = connect_rabbitmq.basic_get('test')
    connect_rabbitmq.basic_ack(method_frame.delivery_tag)
    body_json = json.loads(body)
    assert body_json["method"] == "delete"
    assert body_json["id"] == "1"


@pytest.mark.usefixtures("one_airport_in_db")
def test_update_airport_async(api_client, connect_rabbitmq):
    response = api_client.put("/airports/add-job/1", json=EXAMPLE_AIRPORT)
    method_frame, header_frame, body = connect_rabbitmq.basic_get('test')
    connect_rabbitmq.basic_ack(method_frame.delivery_tag)
    body_json = json.loads(body)
    assert body_json["method"] == "update"
    assert body_json["params"] == EXAMPLE_AIRPORT
    assert body_json["id"] == "1"
