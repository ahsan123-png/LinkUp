# Generated by Django 5.1.2 on 2024-11-30 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userEx', '0004_userex_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userex',
            name='profile_image',
            field=models.ImageField(blank=True, default='static/media/profile.png', null=True, upload_to='profile_images/'),
        ),
    ]
