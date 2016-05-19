# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0013_change_meta_options_on_integrate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_confirmed', models.BooleanField(default=False, verbose_name='Cambio confirmado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('change', models.ForeignKey(default=None, verbose_name='Cambio', to='app.Change')),
                ('user', models.ForeignKey(default=None, verbose_name='Usuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'notifications',
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
    ]
