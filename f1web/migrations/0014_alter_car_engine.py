# Generated by Django 4.2 on 2023-04-19 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0013_alter_driver_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='engine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='f1web.engine'),
        ),
    ]
