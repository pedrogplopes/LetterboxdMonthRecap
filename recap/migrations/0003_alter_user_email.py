# Generated by Django 5.0.1 on 2024-01-08 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recap', '0002_remove_user_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
    ]