from django.contrib import admin

# Register your models here.
from workers_certificates.models import Сertificates, Сertificate_Parts, Сertificate_Users

admin.site.register(Сertificates)
admin.site.register(Сertificate_Parts)
admin.site.register(Сertificate_Users)
