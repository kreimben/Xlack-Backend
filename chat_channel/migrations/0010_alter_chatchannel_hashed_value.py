# Generated by Django 4.1.4 on 2023-01-08 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_channel', '0009_chatchannel_is_dm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatchannel',
            name='hashed_value',
            field=models.CharField(default='2a765d84', max_length=10, unique=True),
        ),
    ]