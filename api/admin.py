from django.contrib import admin
from .models import Deal, Project, DealProject

admin.site.register(Deal)
admin.site.register(Project)
admin.site.register(DealProject)