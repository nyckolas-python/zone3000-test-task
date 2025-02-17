import json
import uuid
from pathlib import Path

import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient

from .models import RedirectRule


def load_fixture(filename):
    """Load test data from a JSON fixture file"""
    fixture_path = Path(__file__).parent / "tests" / "fixtures" / filename
    with open(fixture_path, "r") as f:
        return json.load(f)


@pytest.fixture
def redirect_rules_data():
    """Load redirect rules test data"""
    return load_fixture("redirect_rules.json")


@pytest.fixture
def bulk_create_redirect_rules(auth_client, redirect_rules_data):
    """Create multiple redirect rules from test data"""
    rules = []
    for rule_data in redirect_rules_data["redirect_rules"]:
        response = auth_client.post("/url/", rule_data)
        assert response.status_code == status.HTTP_201_CREATED
        rules.append(response.json())
    return rules


@pytest.mark.django_db
def test_bulk_create_redirect_rules(bulk_create_redirect_rules):
    """Test creating multiple redirect rules from fixture data"""
    rules = bulk_create_redirect_rules
    assert len(rules) == 15  # Updated according to the number of rules in JSON

    # Check the first rule
    assert rules[0]["redirect_url"] == "https://example.com/blog/post1"
    assert rules[0]["is_private"] is False

    # Check the private rule
    assert rules[1]["redirect_url"] == "https://subdomain.example.com/docs"
    assert rules[1]["is_private"] is True

    # Check for redirect_identifier in all rules
    assert all("redirect_identifier" in rule for rule in rules)

    # Check uniqueness of redirect_identifier
    identifiers = [rule["redirect_identifier"] for rule in rules]
    assert len(set(identifiers)) == len(identifiers)


# @pytest.mark.django_db
# def test_list_multiple_redirect_rules(auth_client, bulk_create_redirect_rules):
#     """Test listing multiple redirect rules"""
#     response = auth_client.get("/url/")
#     assert response.status_code == status.HTTP_200_OK
#     results = response.json()["results"]
#     assert len(results) == 15  # Updated according to the number of rules in JSON

#     # Check sorting by created (default)
#     created_dates = [result["created"] for result in results]
#     assert created_dates == sorted(created_dates, reverse=True)


@pytest.fixture
def api_client():
    """Returns an unauthenticated API client"""
    return APIClient()


@pytest.fixture
def user():
    """Creates a test user"""
    return User.objects.create_user(username="testuser", password="password123")


@pytest.fixture
def other_user():
    """Creates another test user"""
    return User.objects.create_user(username="otheruser", password="password123")


@pytest.fixture
def auth_client(user):
    """Returns an authenticated API client"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def redirect_rule(user):
    """Creates a sample redirect rule"""
    return RedirectRule.objects.create(
        id=uuid.uuid4(),
        owner=user,
        redirect_url="https://example.com/new-url/",
        is_private=False,
    )


# @pytest.mark.django_db
# def test_list_redirect_rules(auth_client, redirect_rule):
#     """Tests retrieval of redirect rules"""
#     response = auth_client.get("/url/")
#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.json()["results"]) > 0


@pytest.mark.django_db
def test_create_redirect_rule(auth_client):
    """Tests creating a redirect rule"""
    data = {"redirect_url": "https://google.com", "is_private": False}
    response = auth_client.post("/url/", data)
    assert response.status_code == status.HTTP_201_CREATED

    # Check response data
    assert response.json()["redirect_url"] == "https://google.com"
    assert response.json()["is_private"] is False
    assert "id" in response.json()
    assert "created" in response.json()
    assert "modified" in response.json()
    assert "redirect_identifier" in response.json()

    # Verify UUID format
    uuid_obj = uuid.UUID(response.json()["id"])
    assert str(uuid_obj) == response.json()["id"]

    # Check database record
    rule = RedirectRule.objects.get(id=response.json()["id"])
    assert rule.owner == auth_client.handler._force_user
    assert len(rule.redirect_identifier) == 8


# @pytest.mark.django_db
# def test_get_redirect_rule(auth_client, redirect_rule):
#     """Tests retrieving a single redirect rule"""
#     response = auth_client.get(f"/url/{redirect_rule.id}/")
#     assert response.status_code == status.HTTP_200_OK
#     assert response.json()["redirect_url"] == "https://example.com/new-url/"


@pytest.mark.django_db
def test_update_redirect_rule(auth_client, redirect_rule):
    """Tests updating a redirect rule with PATCH"""
    data = {"is_private": True}
    response = auth_client.patch(f"/url/{redirect_rule.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_private"] is True

    # Check that other fields weren't modified
    assert response.json()["redirect_url"] == redirect_rule.redirect_url
    assert response.json()["id"] == str(redirect_rule.id)
    assert response.json()["redirect_identifier"] == redirect_rule.redirect_identifier


@pytest.mark.django_db
def test_partial_update_redirect_rule(auth_client, redirect_rule):
    """Tests partially updating a redirect rule with PATCH"""
    data = {"is_private": True}
    response = auth_client.patch(f"/url/{redirect_rule.id}/", data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["is_private"] is True


@pytest.mark.django_db
def test_delete_redirect_rule(auth_client, redirect_rule):
    """Tests deleting a redirect rule"""
    response = auth_client.delete(f"/url/{redirect_rule.id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not RedirectRule.objects.filter(id=redirect_rule.id).exists()


@pytest.mark.django_db
def test_permission_denied(api_client, redirect_rule):
    """Tests unauthorized access (unauthenticated user)"""
    response = api_client.get(f"/url/{redirect_rule.id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_other_user_rule(other_user, auth_client, redirect_rule):
    """Tests preventing update by a non-owner user"""
    client = APIClient()
    client.force_authenticate(user=other_user)

    data = {"is_private": True}
    response = client.put(f"/url/{redirect_rule.id}/", data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_private_redirect_rule(auth_client):
    """Tests creating a private redirect rule"""
    data = {"redirect_url": "https://example.com/private/", "is_private": True}
    response = auth_client.post("/url/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["is_private"] is True
    assert "redirect_identifier" in response.json()


@pytest.mark.django_db
def test_redirect_identifier_generation(auth_client):
    """Tests that redirect_identifier is automatically generated"""
    data = {"redirect_url": "https://example.com/test/", "is_private": False}
    response = auth_client.post("/url/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["redirect_identifier"] is not None
    assert len(response.json()["redirect_identifier"]) == 8


@pytest.mark.django_db
def test_redirect_identifier_uniqueness(auth_client):
    """Tests that redirect_identifier is unique"""
    # Create first rule
    data = {"redirect_url": "https://example.com/first/", "is_private": False}
    response1 = auth_client.post("/url/", data)

    # Create second rule
    data["redirect_url"] = "https://example.com/second/"
    response2 = auth_client.post("/url/", data)

    assert (
        response1.json()["redirect_identifier"]
        != response2.json()["redirect_identifier"]
    )


@pytest.mark.django_db
def test_create_redirect_rule_validation(auth_client):
    """Tests validation during redirect rule creation"""
    # Test invalid URL
    data = {"redirect_url": "invalid-url", "is_private": False}
    response = auth_client.post("/url/", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "redirect_url" in response.json()

    # Test missing required field
    data = {"is_private": False}
    response = auth_client.post("/url/", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "redirect_url" in response.json()


@pytest.mark.django_db
def test_update_redirect_rule_validation(auth_client, redirect_rule):
    """Tests validation during redirect rule update"""
    # Test invalid URL
    data = {"redirect_url": "invalid-url"}
    response = auth_client.patch(f"/url/{redirect_rule.id}/", data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "redirect_url" in response.json()
