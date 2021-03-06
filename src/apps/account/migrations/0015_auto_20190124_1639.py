# Generated by Django 2.1.4 on 2019-01-24 16:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20190113_1414'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestdayoffs',
            name='status_changed',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='requestdayoffs',
            name='reason',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='requestdayoffs',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Confirmed'), (2, 'Rejected'), (3, 'Passed')], default=0),
        ),
    ]
