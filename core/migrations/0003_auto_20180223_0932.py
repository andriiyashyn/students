# Generated by Django 2.0.2 on 2018-02-23 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180223_0932'),
    ]

    operations = [
        migrations.RenameField(
            model_name='relationship',
            old_name='destPartyHasRole',
            new_name='destParty',
        ),
        migrations.RenameField(
            model_name='relationship',
            old_name='srcPartyHasRole',
            new_name='srcParty',
        ),
    ]