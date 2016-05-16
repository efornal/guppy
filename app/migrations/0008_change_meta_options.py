# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_add_field_project_to_change'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='change',
            options={'verbose_name': 'Cambio', 'verbose_name_plural': 'Cambios'},
        ),
        migrations.AlterModelOptions(
            name='generated',
            options={'verbose_name': 'Cambios pendientes', 'verbose_name_plural': 'Cambios pendientes'},
        ),
        migrations.AlterModelOptions(
            name='integration',
            options={'verbose_name': 'Integraci\xf3n', 'verbose_name_plural': 'Integraciones'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'Proyecto', 'verbose_name_plural': 'Proyectos'},
        ),
        migrations.AlterModelOptions(
            name='responsable',
            options={'verbose_name': 'Responsable', 'verbose_name_plural': 'Responsable'},
        ),
        migrations.AlterField(
            model_name='change',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='change',
            name='description',
            field=models.TextField(null=True, verbose_name='Descripci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='change',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='change',
            name='project',
            field=models.ForeignKey(default=None, verbose_name='Proyecto', to='app.Project'),
        ),
        migrations.AlterField(
            model_name='change',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='generated',
            name='change',
            field=models.ForeignKey(default=None, verbose_name='Cambio', to='app.Change'),
        ),
        migrations.AlterField(
            model_name='generated',
            name='confirms_change',
            field=models.BooleanField(default=False, verbose_name='Confirma el cambio'),
        ),
        migrations.AlterField(
            model_name='generated',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='generated',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='generated',
            name='user',
            field=models.ForeignKey(default=None, verbose_name='Usuario', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='integration',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='integration',
            name='description',
            field=models.TextField(null=True, verbose_name='Descripci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='integration',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='integration',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(null=True, verbose_name='Descripci\xf3n', blank=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='integration',
            field=models.ForeignKey(default=None, verbose_name='Integraci\xf3n', to='app.Integration'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='confirms_change',
            field=models.BooleanField(default=False, verbose_name='Confirma el cambio'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creado'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='project',
            field=models.ForeignKey(default=None, verbose_name='Proyecto', to='app.Project'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Modificado'),
        ),
        migrations.AlterField(
            model_name='responsable',
            name='user',
            field=models.ForeignKey(default=None, verbose_name='Usuario', to=settings.AUTH_USER_MODEL),
        ),
    ]
