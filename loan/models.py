from django.db import models
from borrower.models import Borrower
from investor.models import Investor
from datetime import datetime, timedelta

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
    interest_rate = models.DecimalField(max_digits=8, decimal_places=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, default='pending')

    def __str__(self):
        return f'{self.investor.user.username} - Loan Request {self.loan_request.pk} - status {self.status}'


LOAN_STATUS_CHOICES = (
    ('funded', 'Funded'),
    ('completed', 'Completed'),
    ('late', 'Late')
)


class Loan(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField()
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, choices=LOAN_STATUS_CHOICES, default='funded')

    def __str__(self):
        return f"Loan {self.pk}"
    
    def create_schedule(self):
        payment_amount = self.installment_amount
        payment_due_date = datetime.today() + timedelta(days=30)
        for i in range(1, self.duration + 1):
            payment = Payment(
                loan=self,
                installment_number=i,
                due_date=payment_due_date,
                amount=payment_amount,
                status='due'
            )
            payment.save()
            payment_due_date += timedelta(days=30)  # Assuming 30 days per installment


PAYMENT_STATUS_CHOICES = (
    ('due', 'Due'),
    ('paid', 'Paid'),
    ('late', 'Late'),
    ('missed', 'Missed'),
)

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    installment_number = models.PositiveIntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='due')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Loan {self.loan.pk} - Installment {self.installment_number}"

