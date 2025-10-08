import pytest
from django.test import Client


def test_fibonacci_view_with_valid_number(client: Client):
    response = client.get("/fibonacci/?n=10")
    assert response.status_code == 200
    assert response.json() == {"result": 55}


def test_fibonacci_view_with_negative_number(client: Client):
    response = client.get("/fibonacci/?n=-1")
    assert response.status_code == 400
    assert response.json() == {
        "error": "Fibonacci sequence is not defined for negative numbers"
    }


def test_fibonacci_view_with_zero(client: Client):
    response = client.get("/fibonacci/?n=0")
    assert response.status_code == 200
    assert response.json() == {"result": 0}


def test_fibonacci_view_with_string_value(client: Client):
    response = client.get("/fibonacci/?n=abc")
    assert response.status_code == 400
    assert response.json() == {
        "error": "Invalid input 'abc'. Parameter 'n' must be an integer."
    }


def test_fibonacci_view_without_n_query_param(client: Client):
    response = client.get("/fibonacci/")
    assert response.status_code == 400
    assert response.json() == {"error": "Query parameter 'n' is required."}


@pytest.mark.slow
@pytest.mark.parametrize("n", [30, 35, 38])
def test_fibonacci_view_stress_test(client: Client, n: int):
    response = client.get(f"/fibonacci/?n={n}")
    assert response.status_code == 200
