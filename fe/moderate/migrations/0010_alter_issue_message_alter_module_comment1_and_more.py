# Generated by Django 4.0.6 on 2022-07-21 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moderate', '0009_alter_issue_message_alter_module_comment1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='message',
            field=models.CharField(default='', max_length=3000),
        ),
        migrations.AlterField(
            model_name='module',
            name='comment1',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='module',
            name='comment2',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='module',
            name='comment3',
            field=models.CharField(default='', max_length=2000),
        ),
        migrations.AlterField(
            model_name='module',
            name='emotions',
            field=models.CharField(default='1.0,1.0,1.0,1.0,1.0', max_length=2000),
        ),
    ]