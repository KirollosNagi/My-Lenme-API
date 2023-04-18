
from django.urls import path
from .views import LoanRequestCreateView, LoanRequestListView, LoanRequestDetailView, LoanOfferListView, \
    LoanOfferCreateView, LoanOfferDetailView

urlpatterns = [
    path('requests/', LoanRequestListView.as_view(), name='loan-request-list'),
    path('requests/new/', LoanRequestCreateView.as_view(), name='loan-request-create'),
    path('requests/<int:pk>/', LoanRequestDetailView.as_view(), name='loan-request-detail'),
    path('offers/', LoanOfferListView.as_view(), name='loan-offer-list'),
    path('offers/new/', LoanOfferCreateView.as_view(), name='loan-offer-create'),
    path('offers/<int:pk>/', LoanOfferDetailView.as_view(), name='loan-offer-detail'),
    path('requests/<int:pk>/offers/', LoanOfferListView.as_view(), name='loan-request-offers-list'),
    #path('offers/<int:pk>/approve/', LoanOfferApproveView.as_view(), name='loan-offer-approve'),

]