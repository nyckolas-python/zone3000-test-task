import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def admin_user():
    """Create an admin user"""
    return User.objects.create_user(
        username='admin',
        password='admin123',
        email='admin@example.com',
        is_staff=True
    )


@pytest.fixture
def regular_user():
    """Create a regular user"""
    return User.objects.create_user(
        username='regular',
        password='regular123',
        email='regular@example.com'
    )


@pytest.fixture
def auth_client():
    """Returns an authenticated API client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def admin_client(auth_client, admin_user):
    """Returns an API client authenticated as admin"""
    auth_client.force_authenticate(user=admin_user)
    return auth_client


@pytest.mark.django_db
def test_create_user_as_admin(admin_client):
    """Test that admin can create new users"""
    data = {
        'username': 'newuser',
        'password': 'newpass123'
    }
    response = admin_client.post(reverse('user-create'), data)
    assert response.status_code == status.HTTP_201_CREATED
    # assert User.objects.count() == 3
    assert response.data['username'] == 'newuser'

    # Verify that user is active by default
    new_user = User.objects.get(username='newuser')
    assert new_user.is_active


@pytest.mark.django_db
def test_create_user_as_regular_user(auth_client, regular_user):
    """Test that regular user cannot create users"""
    auth_client.force_authenticate(user=regular_user)
    data = {
        'username': 'newuser',
        'password': 'newpass123'
    }
    response = auth_client.post(reverse('user-create'), data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_user_as_admin(admin_client, regular_user):
    """Test that admin can update user details"""
    data = {
        'username': 'updated_regular',
        'password': 'newpassword123'
    }
    response = admin_client.put(
        reverse('user-manage', kwargs={'pk': regular_user.pk}),
        data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'updated_regular'


@pytest.mark.django_db
def test_partial_update_user_as_admin(admin_client, regular_user):
    """Test that admin can partially update user details"""
    data = {'username': 'partial_update'}
    response = admin_client.patch(
        reverse('user-manage', kwargs={'pk': regular_user.pk}),
        data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'partial_update'


@pytest.mark.django_db
def test_delete_user_as_admin(admin_client, regular_user):
    """Test that admin can delete users"""
    response = admin_client.delete(
        reverse('user-manage', kwargs={'pk': regular_user.pk})
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_delete_user_as_regular_user(auth_client, regular_user, admin_user):
    """Test that regular user cannot delete users"""
    auth_client.force_authenticate(user=regular_user)
    response = auth_client.delete(
        reverse('user-manage', kwargs={'pk': admin_user.pk})
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_update_user_as_regular_user(auth_client, regular_user, admin_user):
    """Test that regular user cannot update users"""
    auth_client.force_authenticate(user=regular_user)
    data = {'username': 'updated_name'}
    response = auth_client.put(
        reverse('user-manage', kwargs={'pk': admin_user.pk}),
        data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_user_with_invalid_data(admin_client):
    """Test user creation with invalid data"""
    data = {
        'username': '',  # Invalid empty username
        'password': 'pass123'
    }
    response = admin_client.post(reverse('user-create'), data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
