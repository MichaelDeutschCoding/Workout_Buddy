# Generated by Django 3.0.2 on 2020-01-15 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_directmessage_read'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='directmessage',
            options={'default_permissions': ('add',)},
        ),
    ]