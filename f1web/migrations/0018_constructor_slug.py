# Generated by Django 4.2 on 2023-04-20 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0017_alter_engine_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructor',
            name='slug',
            field=models.SlugField(blank=True, max_length=32, null=True),
        ),
    ]
