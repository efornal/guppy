from django.contrib import admin
from app.models import Project
from app.models import Integration
from app.models import Change
from app.models import Responsable
from app.models import Generated
from django.conf.locale.es import formats as es_formats

es_formats.DATETIME_FORMAT = "d-m-Y H:i"


class GeneratedAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_name', 'change',
                    'updated_at', 'created_at', 'confirms_change')
    search_fields = ['change']
    ordering = ('user',)

    
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('project', 'name',
                    'updated_at', 'created_at')
    search_fields = ['name']
    ordering = ('project',)

    
admin.site.register(Integration)
admin.site.register(Project)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Responsable)
admin.site.register(Generated, GeneratedAdmin)
