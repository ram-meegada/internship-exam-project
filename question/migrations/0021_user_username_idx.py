# Generated by Django 4.1.7 on 2023-05-02 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0020_alter_user_username'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='username_idx'),
        ),
    ]
