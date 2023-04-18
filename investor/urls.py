from django.urls import path
from .views import InvestorRegistrationView, InvestorProfileView, InvestorDeactivateView, InvestorListView

urlpatterns = [
    # Investor (admin) list view
    path('list/', InvestorListView.as_view(), name='investor-list'),
    # Investor registration
    path('register/', InvestorRegistrationView.as_view(), name='investor-register'),
    # Investor profile view/update
    path('profile/', InvestorProfileView.as_view(), name='investor-profile'),
    # Investor deactivate profile
    path('deactivate/', InvestorDeactivateView.as_view(), name='investor-deactivate'),
]

