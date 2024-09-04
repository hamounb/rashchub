from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django import views
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .melipayamak import send_token
from django.contrib.auth.mixins import LoginRequiredMixin
from store.models import InvoiceModel, PaymentModel
from django.db.models import Q

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
                    if send is not None:
                        token = TokenModel(
                            user = new_user,
                            user_created = new_user,
                            user_modified = new_user,
                            token = send["code"],
                            status = send["status"],
                            recid = send["recid"]
                        )
                        token.save()
                        messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                        return redirect("accounts:mobile-verify", mobile=new_user.username)
                    return
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
                        if send is not None:
                            token = TokenModel(
                                user = user,
                                user_created = user,
                                user_modified = user,
                                token = send["code"],
                                status = send["status"],
                                recid = send["recid"]
                            )
                            token.save()
                            messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                            return redirect("accounts:mobile-verify", mobile=user.username)
                        return
                    else:
                        send = send_token(number=user.username)
                        if send is not None:
                            token.token = send["code"]
                            token.status = send["status"]
                            token.recid = send["recid"]
                            token.save()
                            messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                            return redirect("accounts:mobile-verify", mobile=user.username)
                        return
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
                login(request, user)
                return redirect("accounts:profile")
            messages.error(request, "رمز یکبارمصرف اشتباه است!")
            return render(request, "accounts/mobile-verify.html", context)
        return render(request, "accounts/mobile-verify.html", context)
    

class TokenSendView(views.View):

    def get(self, request, mobile):
        user = get_object_or_404(User, username=mobile)
        if user.is_active:
            return redirect("")
        try:
            token = TokenModel.objects.get(user__username=mobile)
        except TokenModel.DoesNotExist:
            send = send_token(number=user.username)
            if send is not None:
                token = TokenModel(
                    user = user,
                    user_created = user,
                    user_modified = user,
                    token = send["code"],
                    status = send["status"],
                    recid = send["recid"]
                )
                token.save()
                messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                return redirect("accounts:mobile-verify", mobile=user.username)
            return
        else:
            send = send_token(number=user.username)
            if send is not None:
                token.token = send["code"]
                token.status = send["status"]
                token.recid = send["recid"]
                token.save()
                messages.success(request, "یک پیامک حاوی رمزیکبارمصرف برای شما ارسال شد.")
                return redirect("accounts:mobile-verify", mobile=user.username)
            return
    

class SignInView(views.View):

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect("accounts:profile")
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
                    auth_user = authenticate(username=username, password=password)
                    print(user)
                    if auth_user is not None:
                        login(request, user)
                        return render(request, "accounts/sign-in.html", {"form":form})
                    messages.error(request, "رمز عبور اشتباه است!")
                    return render(request, "accounts/signin.html", {"form":form})
                messages.error(request, "شماره همراه شما در لسیت کاربران وجود ندارد، لطفا ابتدا ثبت نام کنید و بعد وارد شوید")
                return render(request, "accounts/sign-in.html", {"form":form})
        return render(request, "accounts/sign-in.html", {"form":form})
    

class ProfileView(LoginRequiredMixin, views.View):
    login_url = "accounts:sign-in"

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        addresses = AddressModel.objects.filter(user=user)
        invoices = InvoiceModel.objects.filter(user=user)
        total_invoices = invoices.count()
        total_payed = invoices.filter(state=InvoiceModel.STATE_ACCEPT).count()
        total_waiting = invoices.filter(state=InvoiceModel.STATE_WAIT).count()
        payments = PaymentModel.objects.filter(Q(invoice__state=InvoiceModel.STATE_ACCEPT) | Q(invoice__state=InvoiceModel.STATE_DENY) & Q(invoice__is_active=True))
        context = {
            "user":user,
            "addresses":addresses,
            "invoices":invoices,
            "total_invoices":total_invoices,
            "total_payed":total_payed,
            "total_waiting":total_waiting,
            "payments":payments,
        }
        return render(request, "accounts/profile.html", context)
    

class ProfileEditView(LoginRequiredMixin, views.View):
    login_url = "accounts:sign-in"

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = ProfileForm(instance=user)
        return render(request, "accounts/profile-edit.html", {"form":form})
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "اطلاعات کاربری شما با موفقیت ویرایش شد.")
            return redirect("accounts:profile")
        return render(request, "accounts/profile-edit.html", {"form":form})
    

class AddressAddView(LoginRequiredMixin, views.View):
    login_url = "accounts:sign-in"

    def get(self, request):
        form = AddressForm()
        return render(request, "accounts/address-add.html", {"form":form})
    
    def post(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        form = AddressForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.user_modified = user
            obj.user_created = user
            obj.save()
            messages.success(request, "آدرس شما با موفقیت ثبت شد.")
            return redirect("accounts:profile")
        return render(request, "accounts/address-add.html", {"form":form})
    

class AddressEditView(LoginRequiredMixin, views.View):
    login_url = "accounts:sign-in"

    def get(self, request, id):
        address = get_object_or_404(AddressModel, pk=id)
        form = AddressForm(instance=address)
        return render(request, "accounts/address-edit.html", {"form":form})
    
    def post(self, request, id):
        address = get_object_or_404(AddressModel, pk=id)
        user = get_object_or_404(User, pk=request.user.id)
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = user
            obj.user_created = user
            obj.user_modified = user
            obj.save()
            messages.success(request, "آدرس شما با موفقیت ویرایش شد.")
            return redirect("accounts:profile")
        return render(request, "accounts/address-edit.html", {"form":form})