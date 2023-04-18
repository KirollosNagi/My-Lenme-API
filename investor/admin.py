from django.contrib import admin
from .models import Investor
# Register your models here.

class InvestorAdmin(admin.ModelAdmin):
    list_display = ('user','balance',)

admin.site.register(Investor, InvestorAdmin)


