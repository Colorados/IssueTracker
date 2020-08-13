from django.contrib import admin
from issue_tracker.models import Issues, Status, Type

admin.site.register(Issues)
admin.site.register(Type)
admin.site.register(Status)

