from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import SessionHistory, UserProfile, Region
from objects.models import Object
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')

def map_view(request):
    return render(request, 'users/map.html')

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    # Получаем данные для профиля
    user_objects_count = Object.objects.filter(created_by=request.user).count()

    # Сессии за последний месяц
    month_ago = timezone.now() - timedelta(days=30)
    session_count = SessionHistory.objects.filter(
        user=request.user,
        login_time__gte=month_ago
    ).count()

    # Последние 5 сессий
    recent_sessions = SessionHistory.objects.filter(
        user=request.user
    ).order_by('-login_time')[:5]

    # Статистика системы
    total_objects_count = Object.objects.count()
    active_users_count = User.objects.filter(is_active=True).count()
    regions_count = Region.objects.count()

    context = {
        'user_profile': user_profile,
        'user_objects_count': user_objects_count,
        'session_count': session_count,
        'recent_sessions': recent_sessions,
        'total_objects_count': total_objects_count,
        'active_users_count': active_users_count,
        'regions_count': regions_count,
    }

    return render(request, 'users/profile.html', context)