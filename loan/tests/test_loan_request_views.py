from django.urls import reverse
from core.tests.factories import UserFactory
from borrower.tests.factories import BorrowerFactory
from investor.tests.factories import InvestorFactory
from loan.tests.factories import LoanRequestFactory #, LoanOfferFactory, LoanFactory, PaymentFactory
from loan.models import LoanRequest
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
def test_loan_request_list_view_for_user(logged_client):
    # Create a borrower for the loan request
    user1 = UserFactory()
    borrower = BorrowerFactory(user=user1)
    # Generate data for the loan request using the LoanRequestFactory
    loan_request = LoanRequestFactory(borrower=borrower)
    # Use reverse to get the URL for the loan request list view
    response = logged_client.get(reverse('loan-request-list'))
    #shows nothing for users that are neither admin, borrower, or investor
    assert 200 == response.status_code
    assert 0 == len(response.data)
    assert [] == response.json()


@pytest.mark.django_db
def test_loan_request_list_view_for_borrower(logged_client):
    # create a loan request that should not be seen by this borrower
    user1 = UserFactory()
    borrower1 = BorrowerFactory(user=user1)
    loan_request1 = LoanRequestFactory(borrower=borrower1)
    # Create a borrower for the loan request
    borrower = BorrowerFactory(user=logged_client.user)
    # Generate the loan request using the LoanRequestFactory
    loan_request = LoanRequestFactory(borrower=borrower)
    # Use reverse to get the URL for the loan request list view
    response = logged_client.get(reverse('loan-request-list'))

    assert 200 == response.status_code
    assert 1 == len(response.data)
    assert loan_request.id in [request['id'] for request in response.json()]

@pytest.mark.django_db
def test_loan_request_list_view_for_investor(logged_client):
    # Create a 2 loan requests by different users. investor can see both
    user1 = UserFactory()
    borrower1 = BorrowerFactory(user=user1)
    loan_request1 = LoanRequestFactory(borrower=borrower1)
    user2 = UserFactory()
    borrower2 = BorrowerFactory(user=user2)
    loan_request2 = LoanRequestFactory(borrower=borrower2)

    investor = InvestorFactory(user=logged_client.user)
    response = logged_client.get(reverse('loan-request-list'))
    assert 200 == response.status_code
    assert 2 == len(response.data)
    assert loan_request1.id in [request['id'] for request in response.json()]
    assert loan_request2.id in [request['id'] for request in response.json()]



@pytest.mark.django_db
def test_loan_request_list_view_for_borrower_investor(logged_client):
    # Create a 2 loan requests by different users. investor can see both
    user1 = UserFactory()
    borrower1 = BorrowerFactory(user=user1)
    loan_request1 = LoanRequestFactory(borrower=borrower1)
    borrower2 = BorrowerFactory(user=logged_client.user)
    loan_request2 = LoanRequestFactory(borrower=borrower2)

    investor = InvestorFactory(user=logged_client.user)
    response = logged_client.get(reverse('loan-request-list'))
    assert 200 == response.status_code
    assert 2 == len(response.data)
    assert loan_request1.id in [request['id'] for request in response.json()]
    assert loan_request2.id in [request['id'] for request in response.json()]

@pytest.mark.django_db
def test_loan_request_list_view_for_admin(admin_client):
    # Create a 2 loan requests by different users. admin can see both
    user1 = UserFactory()
    borrower1 = BorrowerFactory(user=user1)
    loan_request1 = LoanRequestFactory(borrower=borrower1)
    user2 = UserFactory()
    borrower2 = BorrowerFactory(user=user2)
    loan_request2 = LoanRequestFactory(borrower=borrower2)

    response = admin_client.get(reverse('loan-request-list'))
    assert 200 == response.status_code
    assert 2 == len(response.data)
    assert loan_request1.id in [request['id'] for request in response.json()]
    assert loan_request2.id in [request['id'] for request in response.json()]


@pytest.mark.django_db
def test_loan_request_detail_view(logged_client):
    # Create a loan request for the logged in user
    borrower = BorrowerFactory(user=logged_client.user)
    loan_request = LoanRequestFactory(borrower=borrower)
    # Use reverse to get the URL for the loan request detail view
    response = logged_client.get(reverse('loan-request-detail', args=[loan_request.id]))
    assert 200 == response.status_code
    assert response.data['id'] == loan_request.id
    assert response.data['borrower'] == str(borrower)


@pytest.mark.django_db
def test_loan_request_create_view(logged_client):
    # Create a borrower for the logged in user
    borrower = BorrowerFactory(user=logged_client.user)
    # Create a dictionary of loan request data
    loan_request_data = LoanRequestFactory.build(borrower=borrower).__dict__
    loan_request_data.pop('id')
    loan_request_data.pop('created_at')
    # Use reverse to get the URL for the loan request create view
    response = logged_client.post(reverse('loan-request-create'), data=loan_request_data)
    assert 201 == response.status_code
    assert LoanRequest.objects.filter(id=response.data['id']).exists()

@pytest.mark.django_db
def test_loan_request_create_view_unauthorized(logged_client):
    # Create a borrower for another user
    user1 = UserFactory()
    borrower = BorrowerFactory(user=user1)
    # Create a dictionary of loan request data
    loan_request_data = LoanRequestFactory.build(borrower=borrower).__dict__
    loan_request_data.pop('id')
    loan_request_data.pop('created_at')
    # Use reverse to get the URL for the loan request create view
    response = logged_client.post(reverse('loan-request-create'), data=loan_request_data)
    # non-borrower users are redirected to the borrower register page resulting in 302 (redirect)
    assert 302 == response.status_code