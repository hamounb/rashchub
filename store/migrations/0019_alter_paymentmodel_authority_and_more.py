# Generated by Django 4.2 on 2024-08-16 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_paymentmodel_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmodel',
            name='authority',
            field=models.CharField(blank=True, max_length=36, null=True, verbose_name='شناسه مرجع'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='email',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='ایمیل خریدار'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='invoice',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.invoicemodel', verbose_name='فاکتور'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='mobile',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='شماره تماس خریدار'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='refid',
            field=models.IntegerField(default=0, verbose_name='شماره تراکنش خرید'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='status',
            field=models.IntegerField(default=0, verbose_name='کد وضعیت'),
        ),
    ]
