# Generated by Django 2.2.6 on 2020-03-22 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0020_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mail',
            field=models.EmailField(blank=True, max_length=50),
        ),
    ]