# Generated by Django 2.1.4 on 2018-12-30 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
