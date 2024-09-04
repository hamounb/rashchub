from django import forms
from django.core.exceptions import ValidationError


def is_mobile(value):
    if not str(value).isnumeric() or len(value) !=11 or str(value)[0] != '0':
        raise ValidationError('شماره موبایل صحیح نمی‌باشد!')
    
def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    

class ContactUsForm(forms.Form):
    first_name = forms.CharField(label="نام", required=True, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"نام خود را وارد کنید"}))
    last_name = forms.CharField(label="نام خانوادگی", required=True, widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"نام خانوادگی خود را وارد کنید"}))
    email= forms.EmailField(label="ایمیل", required=False, widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"ایمیل خود را وارد کنید"}))
    mobile = forms.CharField(label="شماره موبایل", required=True, max_length=11, validators=[is_number, is_mobile], widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"موبایل خود را وارد کنید"}))
    message = forms.CharField(label="پیام شما", widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"پیام خود را تایپ کنید", "rows":6}))


class CartSubmitForm(forms.Form):
    price = forms.CharField()


class AddressSelectForm(forms.Form):
    STATE_DEPOSIT = 'deposit'
    STATE_PAID = 'paid'
    STATE_CHOICES = (
        (STATE_DEPOSIT, "پیش پرداخت"),
        (STATE_PAID, "تسویه حساب"),
    )
    address = forms.CharField(widget=forms.RadioSelect())
    amount = forms.CharField(widget=forms.RadioSelect(choices=STATE_CHOICES))


class ProductCommentForm(forms.Form):
    STATE_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    rate = forms.CharField(label="امتیاز", widget=forms.RadioSelect(attrs={"class":"form-control"}, choices=STATE_CHOICES))
    comment = forms.CharField(label="نظر شما", widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"لطفا نظر خود را تایپ کنید", "rows":3}))