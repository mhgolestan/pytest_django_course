import json
import os

import pytest
import requests

companies_url = "http://127.0.0.1:8000/companies/"


@pytest.mark.skipif(os.getenv("CI_SKIP_TEST"), reason="CI skip test")
def test_zero_companies_django_agnostic():
    response = requests.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


@pytest.mark.skipif(os.getenv("CI_SKIP_TEST"), reason="CI skip test")
def test_create_company_django_agnostic():
    response = requests.post(companies_url, data={"name": "Amazon"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Amazon"
    cleanup_company(company_id=response_content.get("id"))


def cleanup_company(company_id: int):
    response = requests.delete(url=f"{companies_url}{company_id}/")
    assert response.status_code == 204
