# Generated by Django 4.2 on 2023-05-19 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0022_alter_car_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='enginemaker',
            name='slug',
            field=models.SlugField(blank=True, max_length=32, null=True),
        ),
    ]