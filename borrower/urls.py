from django.urls import path
from .views import BorrowerRegistrationView, BorrowerProfileView, BorrowerDeactivateView, BorrowerListView

urlpatterns = [
    # Borrower (admin) list view
    path('list/', BorrowerListView.as_view(), name='borrower-list'),
    # Borrower registration
    path('register/', BorrowerRegistrationView.as_view(), name='borrower-register'),
    # Borrower profile view/update
    path('profile/', BorrowerProfileView.as_view(), name='borrower-profile'),
    # Borrower deactivate profile
    path('deactivate/', BorrowerDeactivateView.as_view(), name='borrower-deactivate'),
]

