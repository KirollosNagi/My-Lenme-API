from django.contrib import admin
from .models import LoanRequest, LoanOffer


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'loan_amount')

admin.site.register(LoanRequest, LoanRequestAdmin)

class LoanOfferAdmin(admin.ModelAdmin):
    list_display = ('investor', 'Loan_request')

admin.site.register(LoanOffer, LoanOfferAdmin)
