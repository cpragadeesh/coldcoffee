# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbncc', '0015_auto_20170228_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='time_penalty',
            field=models.IntegerField(default=0),
        ),
    ]
