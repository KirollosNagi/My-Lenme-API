
from django.urls import path
from .views import LoanRequestCreateView, LoanRequestListView, LoanRequestDetailView, \
    LoanOfferListView, LoanOfferCreateView, LoanOfferDetailView, LoanOfferAcceptView, \
    LoanListView, LoanDetailView, PaymentListView, PaymentDetailView

urlpatterns = [
    path('requests/', LoanRequestListView.as_view(), name='loan-request-list'),
    path('requests/new/', LoanRequestCreateView.as_view(), name='loan-request-create'),
    path('requests/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-request-detail'),
    path('offers/', LoanOfferListView.as_view(), name='loan-offer-list'),
    path('offers/new/', LoanOfferCreateView.as_view(), name='loan-offer-create'),
    path('offers/<int:pk>/', LoanOfferDetailView.as_view(), name='loan-offer-detail'),
    path('offers/<int:pk>/accept/', LoanOfferAcceptView.as_view(), name='loan-offer-accept'),
    path('loans/', LoanListView.as_view(), name='loan_list'),
    path('loans/<int:pk>/', LoanDetailView.as_view(), name='loan_detail'),
    path('payments/', PaymentListView.as_view(), name='payment_list'),
    path('payments/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
]