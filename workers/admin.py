from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from workers.models import User, User_Basic_Information, User_Closed_Information
from workers.models.workers_settings import *
from django.utils.translation import gettext_lazy as _

admin.site.register(Subdivision)
admin.site.register(Department)
admin.site.register(Chief)
admin.site.register(User_Basic_Information)
admin.site.register(User_Closed_Information)

class CustomUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('surname', 'name', 'patronymic', 'phone',  'is_staff', 'is_active',)
    list_filter = ('employee', 'is_staff', 'is_active',)
    list_display_links = ('surname', 'name', 'patronymic', 'phone')

    fieldsets = (
        (_('Personal info'), {'fields': (
            'surname', 'name', 'patronymic', 'subdivision', 'department', 'chief')}),
        ('Контакты', {'fields': ('phone', 'email')}),
        ('Увольнение', {'fields': ('employee', 'employee_date')}),
        ('Фото', {'fields': ('image', )}),
        ('Permissions', {'fields': (
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        )}), (_("Important dates"), {"fields": ("last_login", "date_joined")})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('surname', 'name', 'patronymic','email', 'phone', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)

# admin.site.register(Сertificates)
# admin.site.register(Сertificate_Parts)
# admin.site.register(Сertificate_Users)

