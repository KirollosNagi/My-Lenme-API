from django.contrib import admin
from .models import LoanRequest, LoanOffer, Loan, Payment


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'loan_amount')

admin.site.register(LoanRequest, LoanRequestAdmin)

class LoanOfferAdmin(admin.ModelAdmin):
    list_display = ('investor', 'interest_rate')

admin.site.register(LoanOffer, LoanOfferAdmin)


class LoanAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'investor', 'interest_rate')

admin.site.register(Loan, LoanAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('investor', 'interest_rate')

admin.site.register(Payment, PaymentAdmin)