from django.contrib import admin
from app.models import Project
from app.models import Integration
from app.models import Change
from app.models import Responsable
from app.models import Generated
from django.conf.locale.es import formats as es_formats
import logging

es_formats.DATETIME_FORMAT = "d-m-Y H:i"


class GeneratedAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_name', 'change',
                    'updated_at', 'created_at', 'change_confirmed')
    search_fields = ['change']
    ordering = ('user',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'integration_name', 'updated_at', 'created_at',)
    search_fields = ['name']
    ordering = ('name',)
    
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('user', 'project',
                    'updated_at', 'created_at', 'validated_structure')
    search_fields = ['project']
    ordering = ('project',)
    
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('project', 'name',
                    'updated_at', 'created_at')
    search_fields = ['name']
    ordering = ('project',)

    def save_model(self, request, obj, form, change):
        project = Project.objects.get(pk=obj.pk)
        projects = project.integration.project_set.all()
        for p in projects:
            responsable = p.responsable_set.all().first()
            g = Generated(change=obj,user=responsable.user)
            g.save()

            
admin.site.register(Integration)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Generated, GeneratedAdmin)
