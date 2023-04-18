from rest_framework import serializers
from .models import UserProfile, LoanRequest

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'username','full_name', 'address', 'phone_number')



class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = UserProfileSerializer(read_only=True)

    class Meta:
        model = LoanRequest
        fields = ('id', 'borrower', 'loan_amount', 'loan_period', 'created_at', 'status')

