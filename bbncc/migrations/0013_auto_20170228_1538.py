# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-28 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbncc', '0012_auto_20170228_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='penalty_per_line',
            field=models.IntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='problem',
            name='points',
            field=models.IntegerField(default=100),
        ),
    ]