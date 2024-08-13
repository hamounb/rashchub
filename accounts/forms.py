from django import forms
from django.core.exceptions import ValidationError
from .models import AddressModel
from django.contrib.auth.models import User


def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    
def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    
def is_postal(value):
    if len(value) != 10 or not str(value).isnumeric():
        raise ValidationError('کد پستی صحیح نمی‌باشد!')
    

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


class AddressForm(forms.ModelForm):
    postal_code = forms.CharField(max_length=10, required=True, widget=forms.TextInput(attrs={'class':'form-control'}), label="کد پستی", validators=[is_postal])

    class Meta:
        model = AddressModel

        fields = (
                  'province',
                  'city',
                  'postal_code',
                  'address',
                  )
        widgets = {
            'province': forms.TextInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control'}),
            'address': forms.Textarea(attrs={'class':'form-control', 'rows':4}),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = (
                  'first_name',
                  'last_name',
                  'email',
                  )
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
        }