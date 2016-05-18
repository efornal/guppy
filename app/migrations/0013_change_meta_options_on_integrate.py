# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_add_field_projects_to_integration'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='integrate',
            options={'verbose_name': 'Integra', 'verbose_name_plural': 'Integraciones'},
        ),
    ]
