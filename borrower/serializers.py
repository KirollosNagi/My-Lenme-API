from rest_framework import serializers
from .models import Borrower

class BorrowerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Borrower
        fields = ['id','user', 'balance']


