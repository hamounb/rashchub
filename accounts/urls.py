from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("mobile-verify/<str:mobile>/", MobileVerifyView.as_view(), name="mobile-verify"),
    ]