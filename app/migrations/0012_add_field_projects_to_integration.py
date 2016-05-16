# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_relationship_integration'),
    ]

    operations = [
        migrations.AddField(
            model_name='integration',
            name='projects',
            field=models.ManyToManyField(to='app.Project', through='app.Integrate'),
        ),
    ]
