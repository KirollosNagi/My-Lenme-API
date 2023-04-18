from rest_framework import serializers
from .models import Investor

class InvestorSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Investor
        fields = ['id', 'user', 'balance', 'created_at', 'updated_at']
