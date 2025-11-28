from django.urls import path
from . import views

app_name = 'objects'

urlpatterns = [
    path('', views.object_list, name='object_list'),
    path('<int:object_id>/', views.object_detail, name='object_detail'),
    path('regions/', views.region_list, name='region_list'),
    path('sessions/', views.session_history, name='session-history'),
]