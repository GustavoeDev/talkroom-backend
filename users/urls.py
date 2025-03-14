from django.urls import path
from .views import UserSignInView, UserSignUpView, UserView

urlpatterns = [
    path('signin/', UserSignInView.as_view(), name='signin'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('me/', UserView.as_view(), name='user'),
]