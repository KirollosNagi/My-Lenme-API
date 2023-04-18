from django.urls import path
from .views import UserProfileAPIView, LoanRequestListAPIView, RegisterUserAPIView

urlpatterns = [
    path('profile/', UserProfileAPIView.as_view(), name='user_profile'),
    path('loan_requests/', LoanRequestListAPIView.as_view(), name='loan_request_list'),
    path('register/',RegisterUserAPIView.as_view(), name='register'),

]
