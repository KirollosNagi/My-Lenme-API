from django.contrib import admin
from .models import UserProfile, LoanRequest
# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username',)


class LoanRequestAdmin(admin.ModelAdmin):
    list_display = ('borrower', 'loan_amount')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(LoanRequest, LoanRequestAdmin)