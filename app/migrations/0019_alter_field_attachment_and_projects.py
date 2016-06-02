# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_add_field_attachment_to_responsable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integration',
            name='projects',
            field=models.ManyToManyField(to='app.Project', verbose_name='projects', through='app.Integrate'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='attachment',
            field=models.FileField(default=None, upload_to=app.models.responsable_attachment_path, null=True, verbose_name='attachment', blank=True),
        ),
    ]
