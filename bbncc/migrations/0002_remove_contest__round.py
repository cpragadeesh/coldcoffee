# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-03 17:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbncc', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='_round',
        ),
    ]