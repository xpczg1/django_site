from django.contrib import admin
from .models import Regions, Objects, Session_History

@admin.register(Regions)
class RegionsAdmin(admin.ModelAdmin):
    list_display = ('ID_Region', 'Name_Region')
    search_fields = ('Name_Region',)

@admin.register(Objects)
class ObjectsAdmin(admin.ModelAdmin):
    list_display = ('ID_Object', 'Name_Object', 'ID_Region', 'Type_Of_Fence')
    list_filter = ('ID_Region', 'Type_Of_Fence')
    search_fields = ('Name_Object',)

@admin.register(Session_History)
class SessionHistoryAdmin(admin.ModelAdmin):
    list_display = ('ID_Session', 'ID_User', 'ID_Object', 'Date', 'Time')
    list_filter = ('Date', 'ID_User')
    search_fields = ('Main_Guard_Surname',)