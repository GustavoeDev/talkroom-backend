# Generated by Django 5.1.7 on 2025-03-14 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.TextField(default='/media/avatars/avatar-default.png'),
        ),
    ]
