from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from borrower.models import Borrower, LoanRequest
from borrower.serializers import BorrowerSerializer, LoanRequestSerializer
from investor.models import LoanOffer
from investor.serializers import LoanOfferSerializer

class BorrowerRegistrationView(generics.CreateAPIView):
    serializer_class = BorrowerSerializer

class BorrowerProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowerSerializer

    def get_object(self):
        return self.request.user.borrower

class BorrowerDeactivateView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowerSerializer

    def get_object(self):
        return self.request.user.borrower

class BorrowerUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowerSerializer

    def get_object(self):
        return self.request.user.borrower

class LoanRequestCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanRequestSerializer

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user.borrower)

class LoanRequestListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanRequestSerializer

    def get_queryset(self):
        return LoanRequest.objects.filter(borrower=self.request.user.borrower)

class LoanRequestDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanRequestSerializer
    queryset = LoanRequest.objects.all()

class LoanOfferListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return LoanOffer.objects.filter(loan_request__pk=pk)

class LoanOfferApproveView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer
    queryset = LoanOffer.objects.all()

class BorrowerListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()

class AddBalanceView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()
