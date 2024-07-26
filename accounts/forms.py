from django import forms
from django.core.exceptions import ValidationError


def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    
def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    

class SignupForm(forms.Form):
    username = forms.CharField(max_length=11, validators=[is_mobile], label="شماره همراه")
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز عبور")
    password1 = forms.CharField(widget=forms.PasswordInput(), label="تکرار رمز عبور")


class SigninForm(forms.Form):
    username = forms.CharField(max_length=11, validators=[is_mobile], label="شماره همراه")
    password = forms.CharField(widget=forms.PasswordInput(), label="رمز عبور")


class TokenForm(forms.Form):
    first = forms.CharField(max_length=1, required=True, validators=[is_number])
    second = forms.CharField(max_length=1, required=True, validators=[is_number])
    third = forms.CharField(max_length=1, required=True, validators=[is_number])
    fourth = forms.CharField(max_length=1, required=True, validators=[is_number])
    fifth = forms.CharField(max_length=1, required=True, validators=[is_number])
    sixth = forms.CharField(max_length=1, required=True, validators=[is_number])