# Generated by Django 4.2 on 2023-04-19 08:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0010_alter_car_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drive',
            name='team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='f1web.constructor'),
            preserve_default=False,
        ),
    ]
