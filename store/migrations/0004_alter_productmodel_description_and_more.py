# Generated by Django 4.2 on 2024-08-07 12:17

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_productmodel_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='feature',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='ویژگی'),
        ),
    ]
