# Generated by Django 4.2.7 on 2024-05-05 09:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventmanagement', '0009_alter_ticket_date_alter_ticket_purchase_datetime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 5, 12, 31, 0, 613694)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='purchase_datetime',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]
