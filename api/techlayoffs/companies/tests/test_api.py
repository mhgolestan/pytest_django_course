import json
import pytest
from django.test.client import Client
from django.urls import reverse

from companies.models import Company


companies_url = reverse("companies-list")
pytestmark = [pytest.mark.django_db, ]


def test_zero_companies_should_return_empty_list(client: Client) -> None:
    response = client.get(companies_url)
    assert response.status_code == 200
    assert json.loads(response.content) == []


def test_one_company_exits_should_pass(client: Client) -> None:
    test_company = Company.objects.create(name="Amazon")
    response = client.get(companies_url)
    assert response.status_code == 200
    response_content = json.loads(response.content)[0]
    assert response_content.get("name") == test_company.name
    test_company.delete()


def test_create_company_without_argument_should_fail(client: Client) -> None:
    response = client.post(companies_url)
    assert response.status_code == 400


def test_create_existing_company_should_fail(client: Client) -> None:
    Company.objects.create(name="Amazon")
    response = client.post(companies_url, data={"name": "Amazon"})
    assert response.status_code == 400
    Company.objects.get(name="Amazon").delete()


def test_create_company_with_argument_should_pass(client: Client) -> None:
    response = client.post(companies_url, data={"name": "Amazon"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Amazon"
    assert response_content.get("status") == "Hiring"


def test_create_company_with_layoff_status_should_pass(client: Client) -> None:
    response = client.post(companies_url, data={"name": "Amazon", "status": "Layoffs"})
    assert response.status_code == 201
    response_content = json.loads(response.content)
    assert response_content.get("name") == "Amazon"
    assert response_content.get("status") == "Layoffs"
