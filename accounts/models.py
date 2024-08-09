from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    user_modified = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_modified',
        null=True,
        blank=True,
        verbose_name='کاربر ویرایش'
        )
    user_created = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='%(class)s_user_created',
        null=True,
        blank=True,
        verbose_name='کاربر ایجاد'
        )
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ تغییرات', auto_now=True)

    class Meta:
        abstract = True


class TokenModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="کاربر")
    token = models.CharField(verbose_name="رمزیکبارمصرف", max_length=6)
    status = models.CharField(verbose_name="وضعیت", max_length=100)
    recid = models.CharField(verbose_name="شماره پیگیری", max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"
    
    class Meta:
        verbose_name = "رمز یکبارمصرف"
        verbose_name_plural = "رمزهای یکبارمصرف"


class AddressModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    province = models.CharField(verbose_name="استان", max_length=100)
    city = models.CharField(verbose_name="شهر", max_length=100)
    postal_code = models.CharField(verbose_name="کد پستی", max_length=10)
    address = models.TextField(verbose_name="آدرس")

    def __str__(self):
        return f"{self.user.username}[{self.province} - {self.city} ({self.postal_code})]"
    
    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"