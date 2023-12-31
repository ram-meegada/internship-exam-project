# Generated by Django 4.1.7 on 2023-04-19 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam_app', '0006_purchase_purchase_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='timestamp',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
