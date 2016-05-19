# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_copy_generated_to_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generated',
            name='change',
        ),
        migrations.RemoveField(
            model_name='generated',
            name='user',
        ),
        migrations.DeleteModel(
            name='Generated',
        ),
    ]
