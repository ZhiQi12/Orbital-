# Generated by Django 3.1.2 on 2022-06-09 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderateapp', '0002_auto_20220608_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='searched',
            field=models.IntegerField(default=1),
        ),
    ]
