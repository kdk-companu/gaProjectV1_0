from django.contrib import admin

from projects.models import Organization_Direction, Organization, Type_Document
from projects.models.projects import Organizations_Objects, Project, Development_Task, Position_Object, Сabinet

admin.site.register(Organization_Direction)
admin.site.register(Organization)

admin.site.register(Type_Document)

admin.site.register(Organizations_Objects)
admin.site.register(Project)
admin.site.register(Development_Task)
admin.site.register(Position_Object)
admin.site.register(Сabinet)

