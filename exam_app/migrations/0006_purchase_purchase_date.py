# Generated by Django 4.1.7 on 2023-04-18 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0005_delete_blog'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
