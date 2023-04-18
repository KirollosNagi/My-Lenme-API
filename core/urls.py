from django.urls import path
from .views import CreateUserView, LoginView, LogoutView, UserListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user_list'),
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
