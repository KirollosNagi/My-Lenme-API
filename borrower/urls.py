from django.urls import path
from .views import BorrowerRegistrationView, BorrowerProfileView, BorrowerDeactivateView, BorrowerUpdateView, \
    BorrowerListView, AddBalanceView

urlpatterns = [
    # Borrower (admin) list view
    path('list/', BorrowerListView.as_view(), name='borrower-list'),
    # Borrower registration
    path('register/', BorrowerRegistrationView.as_view(), name='register'),
    # Borrower profile view/update
    path('profile/', BorrowerProfileView.as_view(), name='profile'),
    # Borrower deactivate profile
    path('deactivate/', BorrowerDeactivateView.as_view(), name='deactivate'),
    # Borrower update profile
    path('update/', BorrowerUpdateView.as_view(), name='update'),
    # Add balance to borrower's account
    path('add/balance/<int:pk>/', AddBalanceView.as_view(), name='add-balance'),
]

