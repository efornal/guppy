# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_alter_field_attachment_and_projects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integration',
            name='projects',
            field=models.ManyToManyField(to='app.Project', verbose_name='Proyectos', through='app.Integrate'),
        ),
    ]
