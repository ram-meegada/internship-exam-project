# Generated by Django 4.1.7 on 2023-05-01 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0003_testinglistfield'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testinglistfield',
            name='items',
        ),
    ]
