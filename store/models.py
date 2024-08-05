from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from datetime import datetime
import os

# Create your models here.

def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    

def get_image_path(obj, fn):
    ex = os.path.splitext(fn)[1]
    path = datetime.now().strftime(f"images/%Y-%m/%d/{obj.pk}-{ex}")
    return path
    

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


class CategoryModel(BaseModel):
    title = models.CharField(verbose_name="عنوان دسته‌بندی‌", max_length=100, unique=True)
    slug = models.SlugField(verbose_name="آدرس", allow_unicode=True, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی‌ها"


class ColorModel(BaseModel):
    title = models.CharField(verbose_name="عنوان رنگ", max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "رنگ"
        verbose_name_plural = "رنگ‌ها"


class CapacityModel(BaseModel):
    title = models.CharField(verbose_name="تعداد نفرات", max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "ظرفیت"
        verbose_name_plural = "ظرفیت‌ها"


class MaterialModel(BaseModel):
    title = models.CharField(verbose_name="جنس", max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "جنس"
        verbose_name_plural = "جنس‌ها"


class ShapeModel(BaseModel):
    title = models.CharField(verbose_name="شکل میز", max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "شکل"
        verbose_name_plural = "اشکال"


class HashtagModel(BaseModel):
    title = models.CharField(verbose_name="هشتگ", max_length=100, unique=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "هشتگ"
        verbose_name_plural = "هشتگ‌ها"


class ProductModel(BaseModel):
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    category = models.ForeignKey(CategoryModel, verbose_name="دسته‌بندی", on_delete=models.SET_NULL, null=True, blank=True)
    code = models.CharField(verbose_name="کد محصول", max_length=100, null=True, blank=True, unique=True)
    name = models.CharField(verbose_name="نام محصول", max_length=100)
    length = models.CharField(verbose_name="طول", max_length=100, null=True, blank=True)
    width = models.CharField(verbose_name="عرض", max_length=100, null=True, blank=True)
    height = models.CharField(verbose_name="ارتفاع", max_length=100, null=True, blank=True)
    color = models.ManyToManyField(ColorModel, verbose_name="رنگ")
    material = models.ForeignKey(MaterialModel, verbose_name="جنس", on_delete=models.SET_NULL, null=True, blank=True)
    shape = models.ForeignKey(ShapeModel, verbose_name="شکل", on_delete=models.SET_NULL, null=True, blank=True)
    feature = RichTextField(verbose_name="ویژگی", null=True, blank=True)
    view = models.IntegerField(verbose_name="تعداد بازدید", default=0)
    sale = models.IntegerField(verbose_name="تعداد فروش", default=0)
    description = RichTextUploadingField(verbose_name="توضیحات", null=True, blank=True)
    hashtag = models.ManyToManyField(HashtagModel, verbose_name="هشتگ")
    slug = models.SlugField(verbose_name="آدرس", allow_unicode=True, unique=True)

    def __str__(self):
        if self.is_active:
            return f"{self.pk},{self.code}-{self.name}"
        else:
            return f"{self.pk},{self.code}-{self.name}--غیرفعال"
    
    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class ProductImageModel(BaseModel):
    product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="عکس محصول", upload_to=get_image_path)

    def __str__(self):
        return f"{self.pk}-{self.product.name}-{self.image.name}"
    
    class Meta:
        verbose_name = "عکس"
        verbose_name_plural = "عکس‌ها"


class ProductPriceModel(BaseModel):
    product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.CASCADE)
    capacity = models.ForeignKey(CapacityModel, verbose_name="تعداد نفرات", on_delete=models.SET_NULL, null=True, blank=True)
    price = models.CharField(verbose_name="قیمت", max_length=12, validators=[is_number])
    on_sale = models.CharField(verbose_name="تخفیف", max_length=12, validators=[is_number])

    def __str__(self):
        if self.capacity:
            return f"{self.product.name}[{self.capacity.title}] - {self.price}"
        return f"{self.product.name}[نامشخص] - {self.price}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'capacity'], name='price of capacity')
        ]
        verbose_name = "قیمت"
        verbose_name_plural = "قیمت‌ها"


class ProductRateModel(BaseModel):
    product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.CASCADE)
    rate = models.IntegerField(verbose_name="امتیاز", default=0, validators=[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return f"{self.product.name} - {self.rate}"
    
    class Meta:
        ordering = ["-rate", "product"]
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازها"


class ProductCommentModel(BaseModel):
    is_active = models.BooleanField(verbose_name="فعال", default=False)
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.CASCADE)
    comment = models.TextField(verbose_name="متن بازخورد")

    def __str__(self):
        if self.user and self.is_active:
            return f"{self.user.username}-{self.product.name}[{self.created_date}]"
        elif self.user and not self.is_active:
            return f"{self.user.username}-{self.product.name}[{self.created_date}]--غیرفعال"
        elif self.is_active and not self.user:
            return f"نامشخص-{self.product.name}[{self.created_date}]"
        else:
            return f"نامشخص-{self.product.name}[{self.created_date}]--غیرفعال"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'comment'], name='comment of product')
        ]
        ordering = ["-created_date"]
        verbose_name = "بازخورد"
        verbose_name_plural = "بازخوردها"


class InvoiceModel(BaseModel):
    STATE_WAIT = 'wait'
    STATE_ACCEPT = 'accept'
    STATE_DENY = 'deny'
    STATE_CHOICES = (
        (STATE_WAIT, 'در انتظار پرداخت'),
        (STATE_ACCEPT, 'پرداخت شده'),
        (STATE_DENY, 'پرداخت نشده')
    )
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.PROTECT)
    state = models.CharField(verbose_name='وضعیت', max_length=50, choices=STATE_CHOICES, default=STATE_WAIT)
    price = models.CharField(verbose_name="مبلغ", max_length=12, validators=[is_number])
    value_added = models.IntegerField(verbose_name='ارزش افزوده', default=0, validators=[is_number,MinValueValidator(0)])
    total_price = models.CharField(verbose_name='مبلغ کل', max_length=12, validators=[is_number])
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)

    def __str__(self):
        return f"{self.pk}--{self.user.username}--{self.state}--{self.total_price}--{self.created_date}"
    
    class Meta:
        ordering = ["-created_date"]
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"


class InvoiceItemModel(BaseModel):
    invoice = models.ForeignKey(InvoiceModel, verbose_name="فاکتور", on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.PROTECT)
    price = models.CharField(verbose_name="قیمت", max_length=12, validators=[is_number])

    def __str__(self):
        return f"{self.invoice.pk}--{self.invoice.state}--{self.invoice.user.username}"
    
    class Meta:
        ordering = ["-created_date","invoice"]
        verbose_name = "اقلام فاکتور"
        verbose_name_plural = "اقلام فاکتورها"