# Generated by Django 5.0.2 on 2024-02-26 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0014_alter_photo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.ImageField(max_length=254, upload_to='https://https://s3.eu-north-1.amazonaws.com/unit4project-blog/'),
        ),
    ]
