from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from main import views as main_views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Home page
    path('', main_views.home, name='home'),

    # Authentication URLs
    path('register/', main_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # App URLs
    path('profile/', main_views.profile, name='profile'),
    path('profile/edit/', main_views.edit_profile, name='edit_profile'),
    path('map/', main_views.map_view, name='map'),

    # Добавьте оба варианта для совместимости
    path('objects/<int:pk>/', main_views.object_detail, name='object_detail'),
    path('objects/', main_views.object_list, name='object_list'),
    path('api/objects/', main_views.api_objects, name='api_objects'),
]