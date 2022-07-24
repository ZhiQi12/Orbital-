# Generated by Django 3.1.2 on 2022-06-11 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='issue',
            name='message',
            field=models.CharField(default='', max_length=200),
        ),
    ]
