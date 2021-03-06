# Generated by Django 2.2.6 on 2019-12-28 17:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('translate', '0015_remove_comments_reletionships_with_heading'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-date']},
        ),
        migrations.CreateModel(
            name='BlogCommonStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('views', models.IntegerField(default=0, verbose_name='Просмотры')),
                ('blog_key', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='translate.Blog')),
            ],
            options={
                'db_table': 'BlogCommonStatistic',
            },
        ),
    ]
