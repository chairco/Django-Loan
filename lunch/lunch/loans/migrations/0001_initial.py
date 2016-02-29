# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cocodri',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=50)),
                ('email', models.EmailField(verbose_name='email', max_length=254)),
                ('owner', models.ForeignKey(related_name='owned_loan_cocodri', verbose_name='owner', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Cocodri',
                'verbose_name_plural': 'Cocodris',
            },
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('config', models.CharField(max_length=10, blank=True, null=True)),
                ('unit_no', models.CharField(max_length=20, blank=True, null=True)),
                ('isn', models.CharField(verbose_name='ISN', max_length=20, blank=True, null=True)),
                ('failure_symptoms', models.CharField(max_length=300, blank=True, null=True)),
                ('status', models.IntegerField(default=0)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Device',
                'ordering': ['-created_at'],
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='Functionteam',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=30)),
            ],
            options={
                'verbose_name': 'Functionteam',
                'verbose_name_plural': 'Functionteams',
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('purpose', models.CharField(validators=[django.core.validators.RegexValidator(message='Chinese characters are restricted. Must be Alphanumeric                         (只接受英文、數字、半形符號)', code='invalid', regex='^[a-z A-Z 0-9 \\[^\\u4e00-\\u9fa5\\] /,.?~!@#$%^&*()_+]*$')], max_length=100, null=True)),
                ('disassemble', models.BooleanField(verbose_name='Disassemble（會拆機台）', default=False)),
                ('pega_dri_mail_group', models.CharField(verbose_name='Pega DRI Mail Group', max_length=300, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cocodri', models.ForeignKey(related_name='cocodri_item', verbose_name='CoCo DRI', to='loans.Cocodri', null=True)),
                ('function_team', models.ForeignKey(verbose_name='Function Team', to='loans.Functionteam')),
                ('owner', models.ForeignKey(related_name='owned_loans', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Loan',
                'ordering': ['-created_at'],
                'verbose_name_plural': 'Loans',
            },
        ),
        migrations.CreateModel(
            name='Pegadri',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=50)),
                ('email', models.EmailField(verbose_name='email', max_length=254)),
                ('owner', models.ForeignKey(related_name='owned_laon_pegadri', verbose_name='owner', to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Pegadri',
                'verbose_name_plural': 'Pegadris',
            },
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(verbose_name='name', max_length=30)),
            ],
            options={
                'verbose_name': 'Station',
                'verbose_name_plural': 'Stations',
            },
        ),
        migrations.AddField(
            model_name='loan',
            name='pegadri',
            field=models.ForeignKey(related_name='pegadri_item', verbose_name='Pega DRI', to='loans.Pegadri', null=True),
        ),
        migrations.AddField(
            model_name='device',
            name='request',
            field=models.ForeignKey(verbose_name='loan', to='loans.Loan', related_name='menu_items'),
        ),
        migrations.AddField(
            model_name='device',
            name='station',
            field=models.ForeignKey(verbose_name='grpnm', to='loans.Station', related_name='grpnm_items'),
        ),
    ]
