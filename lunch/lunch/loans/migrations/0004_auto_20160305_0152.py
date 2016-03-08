# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_device_sfis_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='grpnm',
            field=models.CharField(blank=True, verbose_name='GRPNM', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='failure_symptoms',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='isn',
            field=models.CharField(verbose_name='ISN', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='device',
            name='station',
            field=models.ForeignKey(related_name='grpnm_items', to='loans.Station', verbose_name='Station'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='disassemble',
            field=models.BooleanField(verbose_name='Disassemble（會拆機台）'),
        ),
    ]
