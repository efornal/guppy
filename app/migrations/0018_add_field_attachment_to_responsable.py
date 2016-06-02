# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_change_meta_options_on_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='responsable',
            name='attachment',
            field=models.FileField(default=None, null=True, upload_to=app.models.responsable_attachment_path, blank=True),
        ),
    ]
