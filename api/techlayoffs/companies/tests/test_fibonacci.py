import pytest
from django.test import Client


def test_fibonacci_view_with_valid_number(client: Client):
    response = client.get("/fibonacci/?n=10")
    assert response.status_code == 200
    assert response.json() == {"result": 55}
    assert response.headers["Content-Type"] == "application/json"


def test_fibonacci_view_with_zero(client: Client):
    response = client.get("/fibonacci/?n=0")
    assert response.status_code == 200
    assert response.json() == {"result": 0}


@pytest.mark.parametrize(
    "query_param, expected_status, expected_response",
    [
        (
            "n=-1",
            400,
            {"error": "Fibonacci sequence is not defined for negative numbers"},
        ),
        (
            "n=abc",
            400,
            {"error": "Invalid input 'abc'. Parameter 'n' must be an integer."},
        ),
        ("", 400, {"error": "Query parameter 'n' is required."}),
    ],
)
def test_fibonacci_view_error_cases(
    client: Client, query_param: str, expected_status: int, expected_response: dict
):
    response = client.get(f"/fibonacci/?{query_param}")
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.slow
@pytest.mark.parametrize("n", [300, 350, 380])
def test_fibonacci_view_stress_test(client: Client, n: int):
    response = client.get(f"/fibonacci/?n={n}")
    assert response.status_code == 200
