from django.shortcuts import render, redirect, get_object_or_404
from django import views
from .forms import *
from .models import TokenModel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .melipayamak import send_token

# Create your views here.

class SignUpView(views.View):

    def get(self, request):
        form = SignUpForm()
        return render(request, "accounts/sign-up.html", {"form":form})
    
    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            password1 = form.cleaned_data.get("password1")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                if password and password1 and password == password1:
                    new_user = User()
                    new_user.username = username
                    new_user.set_password(password)
                    new_user.is_active = False
                    new_user.save()
                    send = send_token(number=username)
                    token = TokenModel(
                        user = new_user,
                        user_created = new_user,
                        user_modified = new_user,
                        token = send['code'],
                        status = send['status']
                    )
                    token.save()
                    messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                    return redirect("accounts:mobile-verify", mobile=new_user.username)
                messages.error(request, "رمز عبور و تکرار رمز عبور باید مشابه باشد!")
                return render(request, "accounts/sign-up.html", {"form":form})
            else:
                if user.is_active:
                    messages.error(request, "با این شماره همراه حساب کاربری ایجاد کرده‌اید، لظفا وارد حساب کاربری شوید.")
                    return render(request, "accounts/sign-up.html", {"form":form})
                if password and password1 and password == password1:
                    user.set_password(password)
                    user.save()
                    try:
                        token = TokenModel.objects.get(user=user)
                    except TokenModel.DoesNotExist:
                        send = send_token(number=user.username)
                        token = TokenModel(
                            user = user,
                            user_created = user,
                            user_modified = user,
                            token = send["code"],
                            status = send["status"]
                        )
                        token.save()
                        messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                        return redirect("accounts:mobile-verify", mobile=user.username)
                    else:
                        send = send_token(number=user.username)
                        token.token = send["code"]
                        token.status = send["status"]
                        token.save()
                        messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                        return redirect("accounts:mobile-verify", mobile=user.username)
                messages.error(request, "رمز عبور و تکرار رمز عبور باید مشابه باشد!")
                return render(request, "accounts/sign-up.html", {"form":form})
        return render(request, "accounts/sign-up.html", {"form":form})
    

class MobileVerifyView(views.View):

    def get(self, request, mobile):
        user = get_object_or_404(User, username=mobile)
        if user.is_active:
            return redirect("accounts:profile")
        form = TokenForm()
        context = {
            "form":form,
            "mobile":mobile
            }
        return render(request, "accounts/mobile-verify.html", context)
    
    def post(self, request, mobile):
        user = get_object_or_404(User, username=mobile)
        if user.is_active:
            return redirect("accounts:profile")
        try:
            token = TokenModel.objects.get(user=user)
        except TokenModel.DoesNotExist:
            return redirect("accounts:sign-up")
        form = TokenForm(request.POST)
        context = {
            "form":form,
            "mobile":mobile,
        }
        if form.is_valid():
            first = form.cleaned_data.get("first")
            second = form.cleaned_data.get("second")
            third = form.cleaned_data.get("third")
            fourth = form.cleaned_data.get("fourth")
            fifth = form.cleaned_data.get("fifth")
            sixth = form.cleaned_data.get("sixth")
            code = f"{first}{second}{third}{fourth}{fifth}{sixth}"
            if token.token == code:
                user.is_active = True
                user.save()
                return redirect("accounts:profile")
            messages.error(request, "رمز یکبارمصرف اشتباه است!")
            return render(request, "accounts/mobile-verify.html", context)
        return render(request, "accounts/mobile-verify.html", context)
    

class SignInView(views.View):

    def get(self, request):
        form = SignInForm()
        return render(request, "accounts/sign-in.html", {"form":form})
    
    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, "شماره همراه شما در لسیت کاربران وجود ندارد، لطفا ابتدا ثبت نام کنید و بعد وارد شوید")
                return render(request, "accounts/sign-in.html", {"form":form})
            else:
                if user.is_active:
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(user)
                        return redirect("accounts:profile")
                    messages.error(request, "رمز عبور اشتباه است!")
                    return render(request, "accounts/signin.html", {"form":form})
                messages.error(request, "شماره همراه شما در لسیت کاربران وجود ندارد، لطفا ابتدا ثبت نام کنید و بعد وارد شوید")
                return redirect("accounts:sign-up")
        return render(request, "accounts/sign-in.html", {"form":form})