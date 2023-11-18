# Generated by Django 4.2.7 on 2023-11-18 00:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_consumptionreader_remaining_validity_days_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumptionreader',
            name='percentage_consumed',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='electricity_pin',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 25, 0, 54, 47, 117823)),
        ),
    ]
