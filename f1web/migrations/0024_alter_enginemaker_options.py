# Generated by Django 4.2 on 2023-05-19 05:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0023_enginemaker_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enginemaker',
            options={'ordering': ('name',)},
        ),
    ]
