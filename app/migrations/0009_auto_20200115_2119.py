# Generated by Django 3.0.2 on 2020-01-15 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_route'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]