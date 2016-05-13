from django.contrib import admin
from app.models import Project
from app.models import Integration
from app.models import Change

admin.site.register(Integration)
admin.site.register(Project)
admin.site.register(Change)


