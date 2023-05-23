# Generated by Django 4.2 on 2023-05-22 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0026_remove_drivingcontract_car_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='carnumber',
            options={'ordering': ('season', 'number')},
        ),
        migrations.AddField(
            model_name='constructor',
            name='is_factory',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='carnumber',
            name='number',
            field=models.IntegerField(blank=True, default=-1),
        ),
    ]