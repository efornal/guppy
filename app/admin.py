#-*- coding: utf-8 -*-
from django.contrib import admin
from app.models import Project
from app.models import Integration
from app.models import Change
from app.models import Responsable
from app.models import Generated
from app.models import Integrate
from django.contrib.auth.models import User
from django.conf.locale.es import formats as es_formats
from django.core.mail import send_mass_mail
import logging
from django.conf import settings
from django.contrib import messages

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

class IntegrateInline(admin.TabularInline):
   model = Integration.projects.through
#   fk_name = "project"
#   fk_name = "integration"
#   fields = ['integrate__project', 'integrate__integration']
   extra = 3
     
class IntegrationAdmin(admin.ModelAdmin):
    #list_display = ('integration', 'project',)
    # search_fields = ['integration']
    # ordering = ('integration',)
    inlines = [IntegrateInline,]

class IntegrateAdmin(admin.ModelAdmin):
    list_display = ('integration', 'project',)

    
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
            
        obj.save()
        integrations = Integration.objects.filter(integrate__project_id=obj.project.pk)
        
        responsible_users=[]
        for i in integrations:
            responsible = User.objects.filter(responsable__project__integrate__integration_id=i.id)
            responsible_users = list(set(responsible_users) | set(responsible)) 

        logging.error("Responsables encontrados: %s" % responsible_users)
        emails=[]
        messages_to_responsible = ()
        link_to_change = "%s%s%s" % (settings.BASE_URL, '/admin/app/change/', obj.pk)
        message_subject = "Actualizacion de '%s'" % obj.project.name
        message_from='noreply@rectorado.unl.edu.ar'
        message_content = "Proyecto actualizado: %s\n\n" % obj.project.name
        message_content += "Cambio: %s\n\n" % obj.name
        message_content += "Descripcion: \n%s\n\n" % obj.description
        message_content += "Creado: %s\n" % obj.created_at.strftime("%d/%m/%Y %H:%M")
        message_content += "Modificado: %s\n" % obj.updated_at.strftime("%d/%m/%Y %H:%M")
        message_content += "Confirmar cambio en: %s\n" % link_to_change

        for u in responsible_users:
            g = Generated(change=obj,user=u)
            g.save()

            if u.email:
                message_to = (message_subject,
                               message_content,
                               message_from,
                               ["%s" % u.email])
                messages_to_responsible += (message_to,)
               
        try:
            sent_messages = send_mass_mail(messages_to_responsible, fail_silently=False)
            messages.info(request, 'Se enviaron %s notificaciones correspondientes a los responsables de proyecto' % sent_messages)
            logging.error("Sent messages:  %s" % sent_messages)
        except Exception as e:
            logging.error("ERROR to sent messajes. %s" % e)

            
admin.site.register(Integration, IntegrationAdmin)
admin.site.register(Integrate,IntegrateAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Generated, GeneratedAdmin)
