# Generated by Django 4.2.7 on 2023-12-08 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='image',
            field=models.ImageField(upload_to='media/news/images'),
        ),
    ]
