from django.test import Client


def test_fibonacci_view_with_valid_number(client: Client):
    response = client.get("/fibonacci/10/")
    assert response.status_code == 200
    assert response.json() == {"result": 55}


def test_fibonacci_view_with_negative_number(client: Client):
    response = client.get("/fibonacci/-1/")
    assert response.status_code == 404


def test_fibonacci_view_with_zero(client: Client):
    response = client.get("/fibonacci/0/")
    assert response.status_code == 200
    assert response.json() == {"result": 0}
