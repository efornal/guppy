from django.contrib import admin
from app.models import Project
from app.models import Integration
from app.models import Change
from app.models import Responsable
from app.models import Generated

admin.site.register(Integration)
admin.site.register(Project)
admin.site.register(Change)
admin.site.register(Responsable)
admin.site.register(Generated)

