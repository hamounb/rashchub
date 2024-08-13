from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign-up"),
    path("sign-in/", SignInView.as_view(), name="sign-in"),
    path("mobile-verify/<str:mobile>/", MobileVerifyView.as_view(), name="mobile-verify"),
    path("token-send/<str:mobile>/", TokenSendView.as_view(), name="token-send"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile-edit"),
    path("address/add/", AddressAddView.as_view(), name="address-add"),
    path("address/edit/<int:id>/", AddressEditView.as_view(), name="address-edit"),
    ]