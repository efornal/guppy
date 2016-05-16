# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_confirms_change_by_change_confirmed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integrate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('integration', models.ForeignKey(default=None, verbose_name='Integraci\xf3n', to='app.Integration')),
            ],
            options={
                'db_table': 'integrate',
                'verbose_name': 'Integrate',
                'verbose_name_plural': 'Integrates',
            },
        ),
        migrations.RemoveField(
            model_name='project',
            name='integration',
        ),
        migrations.AlterField(
            model_name='generated',
            name='change_confirmed',
            field=models.BooleanField(default=False, verbose_name='Cambio confirmado'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='validated_structure',
            field=models.BooleanField(default=False, verbose_name='estructura validada'),
        ),
        migrations.AddField(
            model_name='integrate',
            name='project',
            field=models.ForeignKey(default=None, verbose_name='Proyecto', to='app.Project'),
        ),
    ]
