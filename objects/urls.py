from django.urls import path
from . import views

app_name = 'objects'

urlpatterns = [
    path('', views.object_list, name='object-list'),
    path('<int:object_id>/', views.object_detail, name='object-detail'),
    path('regions/', views.region_list, name='region-list'),
    path('sessions/', views.session_history, name='session-history'),
]