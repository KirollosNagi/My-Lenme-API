from django.urls import reverse
from investor.models import Investor
from investor.tests.factories import UserFactory, InvestorFactory
from decimal import Decimal

import pytest


@pytest.fixture
def logged_client(client):
    user = UserFactory()
    client.login(username=user.username, password='password')
    client.user = user
    return client

@pytest.fixture
def admin_client(client):
    user = UserFactory(is_staff=True, is_superuser=True)
    client.login(username=user.username, password='password')
    client.user = user
    return client


@pytest.mark.django_db
def test_investor_registration_view(logged_client):
    # Send a POST request to the investor registration endpoint with sample data
    response = logged_client.post(reverse('investor-register'), data={'balance': 1000.00})
    # Assert that the response has a 201 status code, indicating a successful creation
    assert response.status_code == 201
    
    # Assert that the user has been assigned as the investor in the response
    assert response.json()['id'] == logged_client.user.id
    
    assert Investor.objects.count() == 1
    investor = Investor.objects.first()
    assert investor.user == logged_client.user
    assert investor.balance == Decimal('1000.00')

    # Clean up objects created during testing
    Investor.objects.filter(user=logged_client.user).delete()


@pytest.mark.django_db
def test_investor_profile_view(logged_client):
    # Create a test investor using the InvestorFactory
    investor = InvestorFactory(user=logged_client.user)

    # Send a GET request to the investor profile endpoint
    response = logged_client.get(reverse('investor-profile'))
    # Assert that the response has a status code of 200 (indicating a successful request)
    assert response.status_code == 200

    # Assert that the response contains the investor object's details
    assert str(investor.balance) in str(response.content)

    # Clean up objects created during testing
    investor.delete()


@pytest.mark.django_db
def test_investor_deactivate_view(logged_client):
    # Create a test investor using the InvestorFactory
    investor = InvestorFactory(user=logged_client.user)

    # Send a DELETE request to the investor deactivate endpoint
    response = logged_client.delete(reverse('investor-deactivate'))

    # Assert that the response has a status code of 204 (indicating a successful deletion)
    assert response.status_code == 204

    # Assert that the investor object has been deleted from the database
    assert not Investor.objects.filter(user=logged_client.user).exists()

    # Clean up objects created during testing
    investor.delete()


@pytest.mark.django_db
def test_investor_list_view_regular_user(logged_client):
    # Create test investors using the InvestorFactory
    response = logged_client.get(reverse('investor-list'))

    # Assert that the response has a status code of 403 (forbidden and available only for admin)
    assert response.status_code == 403


@pytest.mark.django_db
def test_investor_list_view_admin_user(admin_client):
    # Create test investors using the InvestorFactory
    user1 = UserFactory()
    investor1 = InvestorFactory(user=user1)
    user2 = UserFactory()
    investor2 = InvestorFactory(user=user2)

    # Send a GET request to the investor list endpoint
    response = admin_client.get(reverse('investor-list'))

    # Assert that the response has a status code of 200 (indicating a successful request)
    assert response.status_code == 200

    # Assert that the response contains the investors' details
    assert str(investor1.user) in str(response.content)
    assert str(investor2.user) in str(response.content)

    # Clean up objects created during testing
    user1.delete()
    user2.delete()
    investor1.delete()
    investor2.delete() 


