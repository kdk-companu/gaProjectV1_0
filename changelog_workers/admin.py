from django.contrib import admin

from changelog_workers.models import ChangeLog

admin.site.register(ChangeLog)