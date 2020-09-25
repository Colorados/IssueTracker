from django.contrib import admin
from issue_tracker.models import Issues, Status, Type, Project

admin.site.register(Issues)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(Project)

