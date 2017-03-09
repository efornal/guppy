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

class ResponsableProjectListFilter(admin.SimpleListFilter):
    title = _('project')
    parameter_name = 'name'
    default_value = None
    
    def lookups(self, request, model_admin):
        list_of_projects = []
        queryset = Project.objects.all()
        for project in queryset:
            list_of_projects.append(
                (str(project.id), project.name)
            )
        return sorted(list_of_projects, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(project__id=self.value())

    def value(self):
        value = super(ResponsableProjectListFilter, self).value()
        if value is None:
            value = self.default_value
        return value

# class ResponsableProjectListFilter(admin.SimpleListFilter):
#     title = _('responsable')
#     parameter_name = 'name'
#     default_value = None
    
#     def lookups(self, request, model_admin):
#         list_of_users = []
#         queryset = User.objects.all()
#         for user in queryset:
#             list_of_users.append(
#                 (str(user.id), user.username)
#             )
#         return sorted(list_of_users, key=lambda tp: tp[1])
    
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(responsable__user_id=self.value())

#     def value(self):
#         value = super(ResponsableProjectListFilter, self).value()
#         if value is None:
#             value = self.default_value
#         return value


class PeojectIntegrationListFilter(admin.SimpleListFilter):
    title = _('integration')
    parameter_name = 'name'
    default_value = None
    
    def lookups(self, request, model_admin):
        list_of_integrations = []
        queryset = Integration.objects.all()
        for integ in queryset:
            list_of_integrations.append(
                (str(integ.id), integ.name)
            )
        return sorted(list_of_integrations, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(integrate__integration__id=self.value())

    def value(self):
        value = super(PeojectIntegrationListFilter, self).value()
        if value is None:
            value = self.default_value
        return value

    
class ProjectResponsableListFilter(admin.SimpleListFilter):
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
            return queryset.filter(responsable__user_id=self.value())

    def value(self):
        value = super(ProjectResponsableListFilter, self).value()
        if value is None:
            value = self.default_value
        return value

    
class NotificationUserListFilter(admin.SimpleListFilter):
    title = _('user')
    parameter_name = 'user'
    default_value = None

    def __init__(self, request, params, model, model_admin):
        if 'user' not in params: # set default user
            params={'user':'{}'.format(request.user.pk)}
        super(NotificationUserListFilter, self).__init__(
            request, params, model, model_admin)
        
    def lookups(self, request, model_admin):
        notified_projects = Project.objects.filter(responsable__user_id=request.user.pk) \
                                           .distinct()
        projects_users=[]
        for p in notified_projects:
            projects_users.append(p.pk)

        list_of_users = []
        queryset = User.objects.filter(responsable__project_id__in=projects_users)

       
        for user in queryset:
            list_of_users.append(
                (str(user.id), user.username)
            )
        return sorted(list_of_users, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_id=self.value())
        
    def value(self):
        value = super(NotificationUserListFilter, self).value()
        if value is None:
            value = self.default_value
        return value
 

    
class NotificationProjectListFilter(admin.SimpleListFilter):
    title = _('project')
    parameter_name = 'name'
    default_value = None
    
    def lookups(self, request, model_admin):
        list_of_projects = []
        queryset = Project.objects.filter(responsable__user_id=request.user.pk) \
                                  .distinct()
        for project in queryset:
            list_of_projects.append(
                (str(project.id), project.name)
            )
        return sorted(list_of_projects, key=lambda tp: tp[1])
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(change__project__id=self.value())

    def value(self):
        value = super(NotificationProjectListFilter, self).value()
        if value is None:
            value = self.default_value
        return value



class NotificationAdmin(admin.ModelAdmin):
    list_display = ('change', 'user', 'project_name','change_link',
                    'updated_at', 'created_at', 'change_confirmed','disagreement')
    search_fields = ['change']
    ordering = ('user',)
    list_filter = ( NotificationProjectListFilter,NotificationUserListFilter)

    
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
            if obj is None:
                return self.readonly_fields
            if obj.user.pk == request.user.pk:
                if obj.change_confirmed:
                    return ('user', 'change_link', 'change_confirmed','disagreement')
                else:
                    return ('user', 'change_link')
            else:
                return ('user', 'change_link', 'change_confirmed','disagreement')
                

        
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'integrations_name', 'responsable_users', \
                    'updated_at', 'created_at',)
    search_fields = ['name']
    list_filter = (PeojectIntegrationListFilter, ProjectResponsableListFilter)
    ordering = ('name',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ProjectAdmin, self).get_readonly_fields(request, obj)
        else:
            if obj is None:
                return self.readonly_fields
            else:
                if obj.has_as_responsible(request.user.pk):
                    return self.readonly_fields
                else:
                    return ('name', 'description', 'integrations_name',)


    
class IntegrateInline(admin.TabularInline):
   model = Integration.projects.through
   extra = 3



class IntegrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'updated_at', 'created_at', 'confirmed_changes')
    search_fields = ['name']
    ordering = ('name',)

    inlines = [IntegrateInline,]


    
class ResponsableAdmin(admin.ModelAdmin):
    list_display = ('user', 'project',
                    'updated_at', 'created_at', 'validated_structure')
    search_fields = ['project']
    ordering = ('project',)
    list_filter = (ResponsableProjectListFilter, )


        
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
            if obj is None:
                return self.readonly_fields
            if obj.user.pk == request.user.pk:
                if obj.validated_structure:
                    return ('user', 'project', 'attachment', 'validated_structure')
                else:
                    return ('user', 'project')
            else:
                return ('user', 'project', 'attachment', 'validated_structure')
            

    
class ChangeAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'updated_at', 'created_at', 'confirmed_changes')
    search_fields = ['name']
    list_filter = ('project', )
    ordering = ('project',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'rows': 15,})},
    }
 
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return super(ChangeAdmin, self).get_readonly_fields(request, obj)
        else:         
            if obj is None:
                return self.readonly_fields
            else:
                return [field.name for field in Change._meta.fields if field.name != "id"]
            endif
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        change_notifications = Notification.objects.filter(change__id=object_id)
        context = {'notifications': change_notifications,}
        return super(ChangeAdmin, self).change_view(request, object_id,'',context)

    
    def save_model(self, request, obj, form, change):

        if obj.pk:
            obj.save()
            logging.warning('Modifying the change, notifications are omitted...')
            return

        obj.save()

        logging.warning('A new change was created, notifications will be sent.')
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
