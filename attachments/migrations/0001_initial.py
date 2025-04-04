# Generated by Django 5.1.7 on 2025-03-15 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AudioAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.TextField()),
            ],
            options={
                'db_table': 'audio_attachments',
            },
        ),
        migrations.CreateModel(
            name='FileAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('extension', models.CharField(max_length=10)),
                ('size', models.FloatField()),
                ('src', models.TextField()),
                ('content_type', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'file_attachments',
            },
        ),
    ]
