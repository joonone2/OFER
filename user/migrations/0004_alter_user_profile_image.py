# Generated by Django 4.2.5 on 2023-11-16 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(upload_to='user_profile_images/'),
        ),
    ]
