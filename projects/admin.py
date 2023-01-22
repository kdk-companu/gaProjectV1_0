from django.contrib import admin

# Register your models here.
from projects.models import Development_Task, Organization, Organizations_Objects, Objects_Position, Type_Document, \
    Organizations_Objects_Documents, Objects_Position_Documents, Produced_Сabinets

admin.site.register(Organization)
admin.site.register(Organizations_Objects)
admin.site.register(Objects_Position)
admin.site.register(Development_Task)
admin.site.register(Type_Document)
admin.site.register(Organizations_Objects_Documents)
admin.site.register(Objects_Position_Documents)
admin.site.register(Produced_Сabinets)


