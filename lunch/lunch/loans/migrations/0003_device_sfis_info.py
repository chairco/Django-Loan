# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0002_auto_20160301_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='sfis_info',
            field=models.CharField(null=True, blank=True, max_length=40),
        ),
    ]
