# Generated by Django 4.2 on 2023-04-20 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0019_driver_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='car',
            name='slug',
            field=models.SlugField(blank=True, max_length=64, null=True),
        ),
    ]
