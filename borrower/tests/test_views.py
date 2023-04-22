
from django.urls import reverse
from borrower.models import Borrower
from borrower.tests.factories import UserFactory, BorrowerFactory
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
def test_borrower_registration_view(logged_client):
    # Send a POST request to the borrower registration endpoint with sample data
    response = logged_client.post(reverse('borrower-register'), data={'balance': 1000.00})

    # Assert that the response has a status code of 201 (indicating a successful creation)
    assert response.status_code == 201

    # Assert that the user has been assigned as the borrower in the response
    assert response.json()['id'] == logged_client.user.id


    assert Borrower.objects.count() == 1
    investor = Borrower.objects.first()
    assert investor.user == logged_client.user
    assert investor.balance == Decimal('1000.00')

    # Clean up objects created during testing
    Borrower.objects.filter(user=logged_client.user).delete()


@pytest.mark.django_db
def test_borrower_profile_view(logged_client):
    # Create a test borrower using the BorrowerFactory
    borrower = BorrowerFactory(user=logged_client.user)

    # Send a GET request to the borrower profile endpoint
    response = logged_client.get(reverse('borrower-profile'))
    # Assert that the response has a status code of 200 (indicating a successful request)
    assert response.status_code == 200

    # Assert that the response contains the borrower object's details
    assert str(borrower.balance) in str(response.content)

    # Clean up objects created during testing
    borrower.delete()


@pytest.mark.django_db
def test_borrower_deactivate_view(logged_client):
    # Create a test borrower using the BorrowerFactory
    borrower = BorrowerFactory(user=logged_client.user)

    # Send a DELETE request to the borrower deactivate endpoint
    response = logged_client.delete(reverse('borrower-deactivate'))

    # Assert that the response has a status code of 204 (indicating a successful deletion)
    assert response.status_code == 204

    # Assert that the borrower object has been deleted from the database
    assert not Borrower.objects.filter(user=logged_client.user).exists()

    # Clean up objects created during testing
    borrower.delete()


@pytest.mark.django_db
def test_borrower_list_view_regular_user(logged_client):
    # Create test borrowers using the BorrowerFactory
    response = logged_client.get(reverse('borrower-list'))

    # Assert that the response has a status code of 403 (forbidden and available only for admin)
    assert response.status_code == 403


@pytest.mark.django_db
def test_borrower_list_view_admin_user(admin_client):
    # Create test borrowers using the BorrowerFactory
    user1 = UserFactory()
    borrower1 = BorrowerFactory(user=user1)
    user2 = UserFactory()
    borrower2 = BorrowerFactory(user=user2)

    # Send a GET request to the borrower list endpoint
    response = admin_client.get(reverse('borrower-list'))

    # Assert that the response has a status code of 200 (indicating a successful request)
    assert response.status_code == 200

    # Assert that the response contains the borrowers' details
    assert str(borrower1.user) in str(response.content)
    assert str(borrower2.user) in str(response.content)

    # Clean up objects created during testing
    user1.delete()
    user2.delete()
    borrower1.delete()
    borrower2.delete() 