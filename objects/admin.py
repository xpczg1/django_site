from django.contrib import admin
from .models import Category, Object

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'address', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'address', 'description')
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'category', 'description', 'image')
        }),
        ('Геолокация', {
            'fields': ('latitude', 'longitude', 'address')
        }),
    )