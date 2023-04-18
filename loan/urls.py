
from django.urls import path
from .views import LoanRequestCreateView, LoanRequestListView, LoanRequestDetailView, LoanOfferListView, LoanOfferApproveView

urlpatterns = [
    # Loan request create
    path('requests/new/', LoanRequestCreateView.as_view(), name='loan-request-create'),
    # Loan request list
    path('requests/', LoanRequestListView.as_view(), name='loan-request-list'),
    # Loan request detail
    path('requests/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-request-detail'),
    # Loan offer list for a request
    path('requests/<int:pk>/offers/', LoanOfferListView.as_view(), name='loan-offer-list'),
    # Loan offer approve
    #path('offers/<int:pk>/approve/', LoanOfferApproveView.as_view(), name='loan-offer-approve'),
]