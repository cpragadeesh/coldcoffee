# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-17 10:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbncc', '0010_auto_20170217_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 2, 17, 10, 18, 0, 656533)),
        ),
    ]
