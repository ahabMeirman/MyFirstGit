# Generated by Django 2.2.6 on 2019-11-21 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0004_blog_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]