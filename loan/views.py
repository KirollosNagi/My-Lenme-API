
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db.models import Q

from .models import LoanRequest, LoanOffer, Loan, Payment
from .serializers import LoanRequestSerializer, LoanOfferSerializer, LoanSerializer, PaymentSerializer

from decimal import Decimal
from datetime import datetime, timedelta

LENME_FEE = 3.00

class LoanRequestListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or hasattr(user, 'investor'):
            # User is a borrower, return only their loan requests
            return LoanRequest.objects.all()
        elif hasattr(user, 'borrower'):
            # User is an admin, return all loan requests
            return LoanRequest.objects.filter(borrower=user.borrower)
        else:
            # User is neither a borrower nor an admin, return empty queryset
            return LoanRequest.objects.none()


class LoanRequestCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanRequestSerializer

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user.borrower)

class LoanRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LoanRequest.objects.all()
    serializer_class = LoanRequestSerializer



class LoanOfferListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return LoanOffer.objects.all()
        if hasattr(user, 'borrower') and hasattr(user, 'investor'):
            result = LoanOffer.objects.filter(investor=user.investor)
            result |= LoanOffer.objects.filter(loan_request__borrower=user.borrower)
            return result
        if hasattr(user, 'borrower'):
            return LoanOffer.objects.filter(loan_request__borrower=user.borrower)
        elif hasattr(user, 'investor'):
            return LoanOffer.objects.filter(investor=user.investor)
        else:
            return LoanRequest.objects.none()

class LoanOfferCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer
    queryset = LoanOffer.objects.all()

    def perform_create(self, serializer):
        investor = self.request.user.investor
        actual_balance = float(investor.balance - investor.on_hold)
        loan_request = LoanRequest.objects.get(id=self.request.data.get('loan_request'))
        total_amount = float(loan_request.loan_amount) + LENME_FEE
        if actual_balance >= total_amount:
            investor.on_hold += Decimal(total_amount)
            investor.save()
            serializer.save(investor=investor, loan_request=loan_request)
        else:
            raise ValidationError(f"Investor's balance is not sufficient to make the loan offer. add at least ${total_amount-actual_balance} to your balance first")
        

class LoanOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer
    queryset = LoanOffer.objects.all()


class LoanOfferAcceptView(generics.GenericAPIView):
    serializer_class = LoanOfferSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        loan_offer = self.get_loan_offer(pk)

        # Update loan request status to complete
        loan_offer.loan_request.status = 'complete'
        loan_offer.loan_request.save()

        # Update accepted loan offer status to accepted
        loan_offer.status = 'accepted'
        loan_offer.save()

        # Update all other loan offers for the same loan request to rejected
        LoanOffer.objects.filter(loan_request=loan_offer.loan_request).exclude(pk=loan_offer.pk).update(status='rejected')

        # Update investor balance
        loan_offer.investor.balance -= loan_offer.loan_request.loan_amount + Decimal(LENME_FEE)
        loan_offer.investor.on_hold -= loan_offer.loan_request.loan_amount + Decimal(LENME_FEE)
        loan_offer.investor.save()

        # Update borrower balance
        loan_offer.loan_request.borrower.balance += loan_offer.loan_request.loan_amount
        loan_offer.loan_request.borrower.save()

        # Create a new loan object
        loan = Loan()
        loan.borrower = loan_offer.loan_request.borrower
        loan.investor = loan_offer.investor
        loan.initial_amount = loan_offer.loan_request.loan_amount
        loan.interest_rate = loan_offer.interest_rate
        loan.duration = loan_offer.loan_request.loan_period
        loan.status = 'funded'
        current_date = datetime.now().date()
        loan.end_date = current_date + timedelta(days=30*loan.duration)
        loan.remaining_amount = loan.initial_amount * (1+loan.interest_rate)
        loan.installment_amount = loan.initial_amount * (1+loan.interest_rate) / (loan.duration)
        loan.save()
        

        # Create loan schedule
        loan.create_schedule()

        # Serialize loan object and return response
        loan_serializer = LoanSerializer(loan)
        return Response(loan_serializer.data, status=status.HTTP_201_CREATED)

    def get_loan_offer(self, pk):
        # Helper method to retrieve LoanOffer object or raise 404 error
        try:
            return LoanOffer.objects.get(pk=pk)
        except LoanOffer.DoesNotExist:
            raise generics.Http404("LoanOffer not found")
        

class LoanListView(generics.ListCreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Loan.objects.all()
        else:
            queryset = Loan.objects.filter(Q(investor__user=user) | Q(borrower__user=user))
        return queryset

class LoanDetailView(generics.RetrieveAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsAuthenticated]

class PaymentListView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            queryset = Payment.objects.all()
        else:
            queryset = Payment.objects.filter(Q(loan__borrower__user=user) | Q(loan__investor__user=user))
        return queryset

class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        payment = serializer.instance
        old_status = payment.status
        new_status = self.request.data.get('status')
        # if the status is updated
        if old_status != new_status:
            # get the related loan as we may update its status as well and the remaining amount 
            loan = payment.loan
            other_payments = Payment.objects.filter(loan=loan).exclude(pk=payment.pk)
            if new_status == 'paid':
                loan.remaining_amount = loan.installment_amount * other_payments.exclude(status='paid').count()
                if all(payment.status == 'paid' for payment in other_payments):
                    loan.status = 'completed'
                elif all(payment.status not in ['late', 'missed'] for payment in other_payments):
                    loan.status = 'funded'
            elif new_status in ['late', 'missed']:
                loan.remaining_amount = loan.installment_amount * (1 + other_payments.exclude(status='paid').count())
                # the 1+ is to account for this payment as well.
                loan.status = 'late'
        loan.save()
        serializer.save()
