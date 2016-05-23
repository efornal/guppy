# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_change_generated_by_notification_admin'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notification',
            options={'verbose_name': 'Notificaci\xf3n', 'verbose_name_plural': 'Notificaciones'},
        ),
    ]
