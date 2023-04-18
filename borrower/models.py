from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

class LoanRequest(models.Model):
    borrower = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=19, decimal_places=2)
    loan_period = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='active')
