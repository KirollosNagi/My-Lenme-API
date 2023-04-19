from rest_framework import serializers
from .models import LoanRequest, LoanOffer, Loan, Payment
from investor.models import Investor

class LoanRequestSerializer(serializers.ModelSerializer):
    borrower = serializers.StringRelatedField()

    class Meta:
        model = LoanRequest
        fields = ('id', 'borrower', 'loan_amount', 'loan_period', 'created_at', 'status')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        loan_offers = LoanOffer.objects.filter(loan_request__id=instance.pk)
        loan_offers_serializer = LoanOfferSerializer(loan_offers, many=True)
        data['loan_offers'] = loan_offers_serializer.data
        return data
    

class LoanOfferSerializer(serializers.ModelSerializer):
    investor = serializers.PrimaryKeyRelatedField(queryset=Investor.objects.all())
    loan_request = serializers.PrimaryKeyRelatedField(queryset=LoanRequest.objects.all())

    class Meta:
        model = LoanOffer
        fields = ('id', 'investor', 'loan_request', 'interest_rate', 'created_at', 'updated_at', 'status')



class LoanSerializer(serializers.ModelSerializer):
    borrower = serializers.StringRelatedField()
    investor = serializers.StringRelatedField()

    class Meta:
        model = Loan
        fields = ('id', 'borrower', 'investor', 'created_at', 'updated_at', 'end_date', 'initial_amount', 'remaining_amount', 'installment_amount', 'duration', 'interest_rate', 'status')
        read_only_fields = ('id', 'borrower', 'investor', 'created_at', 'updated_at')



class PaymentSerializer(serializers.ModelSerializer):
    loan = serializers.StringRelatedField()

    class Meta:
        model = Payment
        fields = '__all__'