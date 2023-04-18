
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import LoanRequest, LoanOffer
from .serializers import LoanRequestSerializer, LoanOfferSerializer
from rest_framework.response import Response

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

    def get_serializer_context(self):
        # Pass the request user to the serializer context
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context

    def get(self, request, *args, **kwargs):
        # TODO: Fix this view to display related loan offers for this specific loan request.
        # Retrieve the loan request object
        loan_request = self.get_object()
        
        # Get related loan offers
        loan_offers = LoanOffer.objects.filter(loan_request=loan_request)
        
        # Serialize the loan request and loan offers
        serializer = self.get_serializer(loan_request)
        loan_offers_serializer = LoanOfferSerializer(loan_offers, many=True)
        
        # Add the serialized loan offers to the serialized loan request
        serializer.data['loan_offers'] = loan_offers_serializer.data
        
        return Response(serializer.data)

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
            result = LoanOffer.objects.filter(loan_request__borrower=user.borrower)
        elif hasattr(user, 'investor'):
            LoanOffer.objects.filter(investor=user.investor)
        else:
            return LoanRequest.objects.none()

class LoanOfferCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer

    def perform_create(self, serializer):
        serializer.save(investor=self.request.user.investor)

class LoanOfferDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LoanOfferSerializer
    queryset = LoanOffer.objects.all()