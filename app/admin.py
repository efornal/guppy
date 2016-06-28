#-*- coding: utf-8 -*-
from django.contrib import admin
from app.models import Project
from app.models import Integration
from app.models import Change
from app.models import Responsable
from app.models import Notification
from app.models import Integrate
from django.contrib.auth.models import User
from django.conf.locale.es import formats as es_formats
from django.core.mail import send_mass_mail
import logging
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.forms.models import ModelChoiceField
from django.forms.widgets import Textarea
from django.db import models



es_formats.DATETIME_FORMAT = "d-m-Y H:i"


class ResponsableListFilter(admin.SimpleListFilter):
    title = _('user')
    parameter_name = 'user'
    default_value = None
    
    def lookups(self, request, model_admin):
        if not request.user.is_superuser:
            self.default_value = request.user.id
        list_of_users = []
        queryset = User.objects.all()
        for user in queryset:
            list_of_users.append(
                (str(user.id), user.username)
            )
        return sorted(list_of_users, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id=self.value())

    def value(self):
        value = super(ResponsableListFilter, self).value()
        if value is None:
            value = self.default_value
        return value

    
class NotificationListFilter(admin.SimpleListFilter):
    title = _('user')
    parameter_name = 'user'
    default_value = None
    
    def lookups(self, request, model_admin):
        if not request.user.is_superuser:
            self.default_value = request.user.id
        list_of_users = []
        queryset = User.objects.all()
        for user in queryset:
            list_of_users.append(
                (str(user.id), user.username)
            )
        return sorted(list_of_users, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id=self.value())

    def value(self):
        value = super(NotificationListFilter, self).value()
        if value is None:
            value = self.default_value
        return value



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('change', 'user', 'project_name',
                    'updated_at', 'created_at', 'change_confirmed')
    search_fields = ['change']
    ordering = ('user',)
    list_filter = (NotificationListFilter, )

    def save_model(self, request, obj, form, change):
        try:
            if not (request.user == obj.user) and (not request.user.is_superuser):
                raise ValidationError(  _('user_without_permissions') % {'user':request.user.username} )

            obj.save()
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request,"%s" % e[0])

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(NotificationAdmin, self).get_readonly_fields(request, obj)
        else:
            if obj.user.pk == request.user.pk:
                if obj.change_confirmed:
                    return ('user', 'change', 'change_confirmed')
                else:
                    return ('user', 'change')
            else:
                return ('user', 'change', 'change_confirmed')
                


        
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'integrations_name', 'updated_at', 'created_at',)
    search_fields = ['name']
    ordering = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ProjectAdmin, self).get_readonly_fields(request, obj)
        else:
            if obj.has_as_responsible(request.user.pk):
                return ('name', 'integrations_name',)
            else:
                return ('name', 'description', 'integrations_name',)

    
class IntegrateInline(admin.TabularInline):
   model = Integration.projects.through
   extra = 3


   
class IntegrationAdmin(admin.ModelAdmin):
    inlines = [IntegrateInline,]

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(IntegrationAdmin, self).get_readonly_fields(request, obj)
        else:
            return ('name', 'description', 'projects')


    
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('user', 'project',
                    'updated_at', 'created_at', 'validated_structure')
    search_fields = ['project']
    ordering = ('project',)
    list_filter = (ResponsableListFilter, )

        
    def save_model(self, request, obj, form, change):
        try:
            if not (request.user == obj.user) and (not request.user.is_superuser):
                raise ValidationError(  _('user_without_permissions') % {'user':request.user.username} )

            obj.save()
        except ValidationError as e:
            messages.set_level(request, messages.ERROR)
            messages.error(request,"%s" % e[0])

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ResponsableAdmin, self).get_readonly_fields(request, obj)
        else:
            if obj.user.pk == request.user.pk:
                if obj.validated_structure:
                    return ('user', 'project', 'attachment', 'validated_structure')
                else:
                    return ('user', 'project')
            else:
                return ('user', 'project', 'attachment', 'validated_structure')
            

    
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',
                    'updated_at', 'created_at')
    search_fields = ['name']
    ordering = ('project',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 15,})},
    }

    def get_readonly_fields(self, request, obj=None):
         return [field.name for field in Change._meta.fields if field.name != "id"]
     
    def save_model(self, request, obj, form, change):
            
        obj.save()
        integrations = Integration.objects.filter(integrate__project_id=obj.project.pk)
        
        responsible_users=[]
        for i in integrations:
            responsible = User.objects.filter(responsable__project__integrate__integration_id=i.id)
            responsible_users = list(set(responsible_users) | set(responsible)) 

        logging.info("Found responsible: %s" % responsible_users)
        emails=[]
        messages_to_responsible = ()
        link_to_change = "%s%s%s" % (settings.BASE_URL, '/admin/app/change/', obj.pk)
        message_subject = "%s '%s'" % (_('message_updated_project'),obj.project.name)
        message_from = settings.EMAIL_FROM
        message_content = "%s: %s\n\n" % (_('message_updated_project'),obj.project.name)
        message_content += "%s: %s\n\n" % (_('message_change'), obj.name)
        message_content += "%s: \n%s\n\n" % (_('message_description'),obj.description)
        message_content += "%s: %s\n" % (_('message_created_at'),
                                         obj.created_at.strftime("%d/%m/%Y %H:%M"))
        message_content +=  "%s: %s\n" % (_('message_updated_at'),
                                          obj.updated_at.strftime("%d/%m/%Y %H:%M"))
        message_content += "%s: %s\n" % (_('message_confirm_change'),link_to_change)

        for u in responsible_users:
            g = Notification(change=obj,user=u)
            g.save()

            if u.email:
                message_to = (message_subject,
                               message_content,
                               message_from,
                               ["%s" % u.email])
                messages_to_responsible += (message_to,)
               
        try:
            sent_messages = send_mass_mail(messages_to_responsible, fail_silently=False)
            messages.info(request,_('message_mails_sent') % {'emails':sent_messages} )
            logging.info("Sent messages:  %s" % sent_messages)
        except Exception as e:
            logging.error("ERROR to sent messajes. %s" % e)


    # changes the query on the list of projects
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project":
            queryset = Project.objects.filter(responsable__user_id=request.user.id)
            return ModelChoiceField(queryset, initial=None)
        else:
            return super(ChangeAdmin, self).formfield_for_foreignkey(db_field, 
                                                              request, **kwargs)


        
admin.site.register(Integration, IntegrationAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Responsable, ResponsableAdmin)
admin.site.register(Notification, NotificationAdmin)
