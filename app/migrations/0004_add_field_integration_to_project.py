# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_create_model_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='integration',
            field=models.ForeignKey(default=None, verbose_name='integration', to='app.Integration'),
        ),
    ]
