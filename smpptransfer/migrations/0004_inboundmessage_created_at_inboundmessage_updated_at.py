# Generated by Django 4.0.3 on 2022-03-25 10:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smpptransfer', '0003_alter_inboundmessage_is_retrieved'),
    ]

    operations = [
        migrations.AddField(
            model_name='inboundmessage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='inboundmessage',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]