# Generated by Django 2.1.4 on 2019-01-24 16:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20190124_1640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestdayoffs',
            name='status_changed',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]