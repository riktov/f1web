# Generated by Django 4.2 on 2023-04-20 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0016_alter_drivingcontract_options_remove_driver_drives_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='engine',
            options={'ordering': ('maker', 'name')},
        ),
    ]
