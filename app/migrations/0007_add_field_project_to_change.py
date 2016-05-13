# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_create_model_generated'),
    ]

    operations = [
        migrations.AddField(
            model_name='change',
            name='project',
            field=models.ForeignKey(default=None, verbose_name='project', to='app.Project'),
        ),
    ]
