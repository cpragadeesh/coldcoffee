# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-19 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bbncc', '0017_auto_20170219_2357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='output_file_name',
            new_name='output_filename',
        ),
    ]