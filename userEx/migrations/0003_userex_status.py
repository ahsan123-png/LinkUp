# Generated by Django 5.1.2 on 2024-11-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userEx', '0002_userex_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='userex',
            name='status',
            field=models.CharField(blank=True, default='None', max_length=150, null=True),
        ),
    ]
