# Generated by Django 2.0.6 on 2018-06-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20180622_1958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='last_poll',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='poll_date submitted'),
        ),
    ]
