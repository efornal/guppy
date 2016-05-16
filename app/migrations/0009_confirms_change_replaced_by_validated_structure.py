# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_change_meta_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='responsable',
            name='confirms_change',
        ),
        migrations.AddField(
            model_name='responsable',
            name='validated_structure',
            field=models.BooleanField(default=False, verbose_name='validated_structure'),
        ),
    ]
