# Generated by Django 4.1 on 2022-08-21 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_offer_description_offer_photo_alter_auto_brend_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='master',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='master',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
    ]
