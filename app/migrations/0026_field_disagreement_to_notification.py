# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-24 17:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_change_meta_options_and_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='disagreement',
            field=models.BooleanField(default=False, verbose_name='disagreement'),
        ),
    ]
