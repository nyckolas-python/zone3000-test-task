import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from url_management.models import RedirectRule


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
def public_rule(user):
    """Creates a public redirect rule"""
    return RedirectRule.objects.create(
        owner=user,
        redirect_url='https://example.com/public',
        is_private=False
    )


@pytest.fixture
def private_rule(user):
    """Creates a private redirect rule"""
    return RedirectRule.objects.create(
        owner=user,
        redirect_url='https://example.com/private',
        is_private=True
    )


@pytest.mark.django_db
def test_public_redirect_success(api_client, public_rule):
    """Tests successful public redirect without authentication"""
    response = api_client.get(
        reverse('public-redirect', kwargs={
            'redirect_identifier': public_rule.redirect_identifier
        }),
        follow=False
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == 'https://example.com/public'


@pytest.mark.django_db
def test_public_redirect_not_found(api_client):
    """Tests public redirect with non-existent identifier"""
    response = api_client.get(
        reverse('public-redirect', kwargs={
            'redirect_identifier': 'nonexistent'
        })
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_public_redirect_private_rule(api_client, private_rule):
    """Tests public redirect with private rule identifier"""
    response = api_client.get(
        reverse('public-redirect', kwargs={
            'redirect_identifier': private_rule.redirect_identifier
        })
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_private_redirect_success(auth_client, private_rule):
    """Tests successful private redirect for rule owner"""
    response = auth_client.get(
        reverse('private-redirect', kwargs={
            'redirect_identifier': private_rule.redirect_identifier
        }),
        follow=False
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert response.url == 'https://example.com/private'


@pytest.mark.django_db
def test_private_redirect_unauthorized(api_client, private_rule):
    """Tests private redirect without authentication"""
    response = api_client.get(
        reverse('private-redirect', kwargs={
            'redirect_identifier': private_rule.redirect_identifier
        })
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_private_redirect_wrong_user(other_user, private_rule):
    """Tests private redirect with non-owner user"""
    client = APIClient()
    client.force_authenticate(user=other_user)
    response = client.get(
        reverse('private-redirect', kwargs={
            'redirect_identifier': private_rule.redirect_identifier
        })
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_private_redirect_not_found(auth_client):
    """Tests private redirect with non-existent identifier"""
    response = auth_client.get(
        reverse('private-redirect', kwargs={
            'redirect_identifier': 'nonexistent'
        })
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_private_redirect_public_rule(auth_client, public_rule):
    """Tests private redirect with public rule identifier"""
    response = auth_client.get(
        reverse('private-redirect', kwargs={
            'redirect_identifier': public_rule.redirect_identifier
        })
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
