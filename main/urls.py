from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from main import views as main_views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls),

    # Home page
    path('', main_views.home, name='home'),

    # Authentication URLs
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    # App URLs
    path('profile/', user_views.profile, name='profile'),
    path('map/', user_views.map_view, name='map'),
    path('objects/', main_views.object_list, name='object-list'),
]