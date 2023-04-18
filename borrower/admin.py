from django.contrib import admin
from .models import Borrower
# Register your models here.

class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('user','balance',)

admin.site.register(Borrower, BorrowerAdmin)


