from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path("sign-up/", SignupView.as_view(), name="sign-up"),
    path("sign-in/", SigninView.as_view(), name="sign-in"),
    path("mobile-verify/", MobileVerifyView.as_view(), name="mobile-verify"),
    ]