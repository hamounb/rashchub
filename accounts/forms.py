from django import forms
from django.core.exceptions import ValidationError


def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    
def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=11, validators=[is_mobile], label="شماره همراه", widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"شماره همراه"}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"رمز عبور"}))
    password1 = forms.CharField(label="تکرار رمز عبور", widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"تکرار رمز عبور"}))


class SignInForm(forms.Form):
    username = forms.CharField(max_length=11, validators=[is_mobile], label="شماره همراه",  widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"شماره همراه"}))
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"رمز عبور"}))


class TokenForm(forms.Form):
    first = forms.CharField(max_length=1, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))
    second = forms.CharField(max_length=1, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))
    third = forms.CharField(max_length=1, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))
    fourth = forms.CharField(max_length=1, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))
    fifth = forms.CharField(max_length=1, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))
    sixth = forms.CharField(max_length=1, required=True, validators=[is_number],  widget=forms.TextInput(attrs={"class":"text-center form-control rounded"}))