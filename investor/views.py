from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Investor
from .serializers import InvestorSerializer

class InvestorRegistrationView(generics.CreateAPIView):
    serializer_class = InvestorSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_user(self):
        return self.request.user

class InvestorProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvestorSerializer

    def get_object(self):
        return self.request.user.investor

class InvestorDeactivateView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = InvestorSerializer

    def get_object(self):
        return self.request.user.investor

class InvestorListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = InvestorSerializer
    queryset = Investor.objects.all()

