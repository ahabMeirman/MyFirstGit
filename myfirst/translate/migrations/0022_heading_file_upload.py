# Generated by Django 2.2.6 on 2020-03-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0021_userprofile_mail'),
    ]

    operations = [
        migrations.AddField(
            model_name='heading',
            name='file_upload',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
