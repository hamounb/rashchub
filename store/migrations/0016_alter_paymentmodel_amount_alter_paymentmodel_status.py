# Generated by Django 4.2 on 2024-08-14 18:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_paymentmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmodel',
            name='amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='مبلغ'),
        ),
        migrations.AlterField(
            model_name='paymentmodel',
            name='status',
            field=models.IntegerField(verbose_name='وضعیت'),
        ),
    ]
