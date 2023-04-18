from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import UserProfile, LoanRequest
from .serializers import UserProfileSerializer, LoanRequestSerializer

from rest_framework_simplejwt.tokens import RefreshToken

#Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": serializer.data,
        }
        return Response(res, status.HTTP_201_CREATED)
    

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.userprofile


class LoanRequestListAPIView(generics.ListCreateAPIView):
    serializer_class = LoanRequestSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return LoanRequest.objects.filter(borrower=self.request.user.userprofile)

    def perform_create(self, serializer):
        serializer.save(borrower=self.request.user.userprofile)
