from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from borrower.models import Borrower
from borrower.serializers import BorrowerSerializer

class BorrowerRegistrationView(generics.CreateAPIView):
    serializer_class = BorrowerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_user(self):
        return self.request.user

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

class BorrowerListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()

