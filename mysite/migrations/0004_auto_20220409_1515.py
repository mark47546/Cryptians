# Generated by Django 3.2 on 2022-04-09 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_tweet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='is_active',
        ),
        migrations.AddField(
            model_name='tweet',
            name='tweets_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]