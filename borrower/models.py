from django.db import models
from django.contrib.auth.models import User

class Borrower(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # we can add the extra fields later
    # phone_number = models.CharField(max_length=15)          # Assuming maximum length of 15 for phone number
    # address = models.TextField()

    def __str__(self):
        return f'borrower: {self.user.username}'