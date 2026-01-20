from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Roles, Users, Regions, Objects, Session_History

@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = ('ID_Role', 'Name_Role')
    search_fields = ('Name_Role',)

@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    list_display = ('Login', 'Name', 'Surname', 'ID_Role', 'is_active')
    list_filter = ('ID_Role', 'is_active')
    fieldsets = (
        (None, {'fields': ('Login', 'password')}),
        ('Персональная информация', {'fields': ('Name', 'Surname', 'Patronymic', 'ID_Role')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('Login', 'Name', 'Surname', 'Patronymic', 'ID_Role', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    search_fields = ('Login', 'Name', 'Surname')
    ordering = ('Login',)

# Зарегистрируйте остальные модели
admin.site.register(Regions)
admin.site.register(Objects)
admin.site.register(Session_History)