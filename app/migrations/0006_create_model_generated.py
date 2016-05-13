# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0005_create_model_responsable'),
    ]

    operations = [
        migrations.CreateModel(
            name='Generated',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('confirms_change', models.BooleanField(default=False, verbose_name='confirms_change')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('change', models.ForeignKey(default=None, verbose_name='change', to='app.Change')),
                ('user', models.ForeignKey(default=None, verbose_name='usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'generated',
                'verbose_name': 'Generated',
                'verbose_name_plural': 'Generated',
            },
        ),
    ]
