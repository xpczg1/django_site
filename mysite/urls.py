from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.home, name='home'),
    path('map/', views.map_view, name='map'),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),

    # URL для объектов
    path('objects/', views.object_list, name='object-list'),
    path('objects/<int:object_id>/', views.object_detail, name='object-detail'),
    path('regions/', views.region_list, name='region-list'),
    path('sessions/', views.session_history, name='session-history'),

    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
]