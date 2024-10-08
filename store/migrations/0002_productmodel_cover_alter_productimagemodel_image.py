# Generated by Django 4.2 on 2024-08-07 11:32

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=store.models.get_cover_path, verbose_name='عکس کاور'),
        ),
        migrations.AlterField(
            model_name='productimagemodel',
            name='image',
            field=models.FileField(upload_to=store.models.get_image_path, verbose_name='عکس محصول'),
        ),
    ]
