# Generated by Django 4.2 on 2023-04-20 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('f1web', '0015_drivingcontract'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='drivingcontract',
            options={'ordering': ('season', 'team', 'driver')},
        ),
        migrations.RemoveField(
            model_name='driver',
            name='drives',
        ),
        migrations.AlterField(
            model_name='drivingcontract',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='f1web.driver'),
        ),
        migrations.AlterField(
            model_name='drivingcontract',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='f1web.season'),
        ),
        migrations.AlterField(
            model_name='drivingcontract',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='drives', to='f1web.constructor'),
        ),
        migrations.DeleteModel(
            name='Drive',
        ),
    ]
