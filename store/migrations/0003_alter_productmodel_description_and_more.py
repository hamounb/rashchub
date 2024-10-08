# Generated by Django 4.2 on 2024-08-07 12:02

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_productmodel_cover_alter_productimagemodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='description',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='توضیحات'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='feature',
            field=django_ckeditor_5.fields.CKEditor5Field(verbose_name='ویژگی'),
        ),
    ]
