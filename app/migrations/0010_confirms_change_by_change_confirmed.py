# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_confirms_change_replaced_by_validated_structure'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generated',
            name='confirms_change',
        ),
        migrations.AddField(
            model_name='generated',
            name='change_confirmed',
            field=models.BooleanField(default=False, verbose_name='change_confirmed'),
        ),
    ]
