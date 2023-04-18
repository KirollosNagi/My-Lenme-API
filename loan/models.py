from django.db import models
from borrower.models import Borrower
from investor.models import Investor

class LoanRequest(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=19, decimal_places=2)
    loan_period = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='active')

    def __str__(self):
        return f'id: {self.pk} - {self.borrower.user.username} - Loan amount {self.loan_amount} - loan period {self.loan_period} - status {self.status}'


class LoanOffer(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    loan_request = models.ForeignKey(LoanRequest, on_delete=models.CASCADE)
    interest_rate = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=255, default='pending')

    def __str__(self):
        return f'{self.investor.user.username} - Loan Request {self.loan_request.pk} - status {self.status}'
