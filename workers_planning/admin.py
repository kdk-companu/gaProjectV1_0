from django.contrib import admin

# Register your models here.
from workers_planning.models import Information_Missing, Information_Schedule, Workers_Missing, Workers_Mission, \
    Workers_Weekend_Work, Workers_Mission_Report_File, Workers_Mission_Report

admin.site.register(Information_Missing)
admin.site.register(Information_Schedule)
admin.site.register(Workers_Missing)
admin.site.register(Workers_Mission)
admin.site.register(Workers_Weekend_Work)
admin.site.register(Workers_Mission_Report)
admin.site.register(Workers_Mission_Report_File)




