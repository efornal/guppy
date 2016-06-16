# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0021_add_field_comment_to_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='comment',
            field=models.TextField(null=True, verbose_name='Comentario', blank=True),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='attachment',
            field=models.FileField(default=None, upload_to=app.models.responsable_attachment_path, null=True, verbose_name='Archivo adjunto', blank=True),
        ),
    ]
