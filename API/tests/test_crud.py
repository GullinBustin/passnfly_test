import pytest
from flask_sqlalchemy import inspect

from tests.fixtures import EXAMPLE_AIRPORT, CSV_AIRPORTS


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}


@pytest.mark.usefixtures("clean_airports")
def test_add_airport(api_client, airport_model):
    response = api_client.post("/airports/", json=EXAMPLE_AIRPORT)
    data = response.json
    assert data == {**EXAMPLE_AIRPORT, "id": 1}
    asset = object_as_dict(airport_model.query.first())
    assert data == asset


@pytest.mark.usefixtures("clean_airports")
def test_empty_get(api_client):
    response = api_client.get("/airports/")
    data = response.json
    assert data == []


@pytest.mark.usefixtures("one_airport_in_db")
def test_get_one_airport(api_client):
    response = api_client.get("/airports/")
    data = response.json
    assert data == [{**EXAMPLE_AIRPORT, "id": 1}]


@pytest.mark.usefixtures("one_airport_in_db")
def test_delete_airport(api_client, airport_model):
    response = api_client.delete("/airports/1")
    assets = airport_model.query.all()
    assert assets == []


@pytest.mark.usefixtures("one_airport_in_db")
def test_update_airport(api_client, airport_model):
    response = api_client.put("/airports/1", json=CSV_AIRPORTS[0])
    data = response.json
    assert data == {**CSV_AIRPORTS[0], "id": 1}
    assets = airport_model.query.all()
    assert object_as_dict(assets[0]) == data


@pytest.mark.usefixtures("clean_airports")
def test_csv_post(api_client, airport_model):
    with open("tests/airports_test.csv", "rb") as a_file:
        data = {"file": (a_file, "airports.csv")}
        response = api_client.post("/airports/csv", data=data)
    assets = airport_model.query.all()
    for index in range(len(assets)):
        assert object_as_dict(assets[index]) == CSV_AIRPORTS[index]

