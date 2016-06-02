from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
import logging


class Project(models.Model):
    id = models.AutoField( primary_key=True,null=False)
    name = models.CharField( max_length=200,null=False,
                             verbose_name=_('name'))
    description = models.TextField( null=True, blank=True,
                                    verbose_name=_('description'))
    created_at = models.DateTimeField( auto_now_add=True,
                                       verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,
                                       verbose_name=_('updated_at'))

    class Meta:
        db_table = 'projects'
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def __unicode__(self):
        return "%s" % (self.name)
    
    def integration_name(obj):
        return "%s" % obj.name

    def has_as_responsible(self,user_id):
        projects = Project.objects.filter(responsable__user_id=user_id).filter(pk=self.pk)
        if len(projects) > 0:
            return True
        return False

    
class Integration(models.Model):
    id = models.AutoField( primary_key=True,null=False)
    name = models.CharField( max_length=200,null=False,
                             verbose_name=_('name'))
    description = models.TextField( null=True, blank=True,
                                    verbose_name=_('description'))
    created_at = models.DateTimeField( auto_now_add=True,
                                       verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,
                                       verbose_name=_('updated_at'))
    projects = models.ManyToManyField(Project, through='Integrate')

    class Meta:
        db_table = 'integrations'
        verbose_name = _('Integration')
        verbose_name_plural = _('Integrations')

    def __unicode__(self):
        return "%s" % (self.name)

class Change(models.Model):
    id = models.AutoField( primary_key=True,null=False)
    name = models.CharField( max_length=200,null=False,
                             verbose_name=_('name'))
    description = models.TextField( null=True, blank=True,
                                    verbose_name=_('description'))
    created_at = models.DateTimeField( auto_now_add=True,
                                       verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,
                                       verbose_name=_('updated_at'))
    project = models.ForeignKey(Project, null=False, default=None,
                                    verbose_name=_('project'))

    class Meta:
        db_table = 'changes'
        verbose_name = _('Change')
        verbose_name_plural = _('Changes')

    def __unicode__(self):
        return "%s" % (self.name)
    
def responsable_attachment_path(instance, filename):
    return 'responsable_{0}/{1}'.format(instance.id, filename)

class Responsable(models.Model):
    validated_structure = models.BooleanField(default=False,
                                              verbose_name=_('validated_structure'))
    created_at = models.DateTimeField( auto_now_add=True,
                                       verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,
                                       verbose_name=_('updated_at'))
    project = models.ForeignKey(Project, null=False, default=None,
                                    verbose_name=_('project'))
    user = models.ForeignKey(User, null=False, default=None,
                                    verbose_name=_('user'))
    attachment = models.FileField(default=None, null=True, blank=True,
                                  upload_to=responsable_attachment_path)
    
    class Meta:
        db_table = 'responsible'
        verbose_name = _('Responsable')
        verbose_name_plural = _('responsible')

    def __unicode__(self):
        return "%s %s %s" % (self.user.username,_('of'),self.project.name)


class Notification(models.Model):
    change_confirmed = models.BooleanField(default=False,
                                          verbose_name=_('change_confirmed'))
    created_at = models.DateTimeField( auto_now_add=True,
                                       verbose_name=_('created_at'))
    updated_at = models.DateTimeField( auto_now=True,
                                       verbose_name=_('updated_at'))
    change = models.ForeignKey(Change, null=False, default=None,
                                    verbose_name=_('change'))
    user = models.ForeignKey(User, null=False, default=None,
                                    verbose_name=_('user'))
    def project_name(obj):
        return "%s" % obj.change.project.name

    class Meta:
        db_table = 'notifications'
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')

    def __unicode__(self):
        return "%s %s %s" % (self.change.name,_('by'),self.user.username)


class Integrate(models.Model):
    project = models.ForeignKey(Project, null=False, default=None,
                                verbose_name=_('project'))
    integration = models.ForeignKey(Integration, null=False, default=None,
                                    verbose_name=_('integration'))

    class Meta:
        db_table = 'integrate'
        verbose_name = _('Integrate')
        verbose_name_plural = _('Integrates')

    def __unicode__(self):
        return "%s" % (self.id)
