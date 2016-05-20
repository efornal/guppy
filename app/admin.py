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

es_formats.DATETIME_FORMAT = "d-m-Y H:i"


class ResponsableListFilter(admin.SimpleListFilter):
    title = _('user')
    parameter_name = 'user'
    default_value = None
    
    def lookups(self, request, model_admin):
        self.default_value = request.user.id
        list_of_users = []
        queryset = User.objects.all()
        for user in queryset:
            list_of_users.append(
                (str(user.id), user.username)
            )
        return sorted(list_of_users, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        self.default_value = request.user.id
        if self.value():
            return queryset.filter(user_id=self.value())

    def value(self):
        value = super(ResponsableListFilter, self).value()
        if value is None:
            if self.default_value is None:
                first_record = User.objects.order_by('username').first()
                value = None if first_record is None else first_record.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)

    
    
class NotificationListFilter(admin.SimpleListFilter):
    title = _('user')
    parameter_name = 'user'
    default_value = None
    
    def lookups(self, request, model_admin):
        self.default_value = request.user.id
        list_of_users = []
        queryset = User.objects.all()
        for user in queryset:
            list_of_users.append(
                (str(user.id), user.username)
            )
        return sorted(list_of_users, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        self.default_value = request.user.id
        if self.value():
            return queryset.filter(user_id=self.value())

    def value(self):
        value = super(NotificationListFilter, self).value()
        if value is None:
            if self.default_value is None:
                first_record = User.objects.order_by('username').first()
                value = None if first_record is None else first_record.id
                self.default_value = value
            else:
                value = self.default_value
        return str(value)


    
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


        
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'integration_name', 'updated_at', 'created_at',)
    search_fields = ['name']
    ordering = ('name',)


    
class IntegrateInline(admin.TabularInline):
   model = Integration.projects.through
   extra = 3


   
class IntegrationAdmin(admin.ModelAdmin):
    inlines = [IntegrateInline,]


    
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



class ChangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'project',
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
