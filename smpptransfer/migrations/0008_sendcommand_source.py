# Generated by Django 4.0.3 on 2022-03-26 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smpptransfer', '0007_sendcommand_created_at_sendcommand_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='sendcommand',
            name='source',
            field=models.CharField(default='Chiweto', max_length=30),
        ),
    ]
