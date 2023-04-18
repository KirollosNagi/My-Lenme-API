from rest_framework import serializers
from .models import LoanRequest, LoanOffer
# from borrower.serializers import BorrowerSerializer
from investor.models import Investor

class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = serializers.StringRelatedField()

    class Meta:
        model = LoanRequest
        fields = ('id', 'borrower', 'loan_amount', 'loan_period', 'created_at', 'status')



class LoanOfferSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(queryset=Investor.objects.all())
    loan_request = serializers.PrimaryKeyRelatedField(queryset=LoanRequest.objects.all())

    class Meta:
        model = LoanOffer
        fields = ('id', 'investor', 'loan_request', 'interest_rate', 'created_at', 'updated_at', 'status')