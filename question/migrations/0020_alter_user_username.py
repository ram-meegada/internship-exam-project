# Generated by Django 4.1.7 on 2023-05-02 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0019_alter_answerquestion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=255, unique=True),
        ),
    ]
