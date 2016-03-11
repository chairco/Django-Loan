# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='sfis_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='device',
            name='utk',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
