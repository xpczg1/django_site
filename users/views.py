from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count
from datetime import datetime, timedelta

# Импортируем модели из objects приложения
from objects.models import Objects, Regions, Session_History


def home(request):
    """Главная страница"""
    try:
        total_objects = Objects.objects.count()
        total_regions = Regions.objects.count()
        total_sessions = Session_History.objects.count()
    except Exception as e:
        # Если база данных еще не готова
        total_objects = total_regions = total_sessions = 0

    context = {
        'total_objects': total_objects,
        'total_regions': total_regions,
        'total_sessions': total_sessions,
    }
    return render(request, 'users/home.html', context)


def register(request):
    """Регистрация пользователя"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Аккаунт создан для {user.username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def map_view(request):
    """Карта объектов"""
    objects = Objects.objects.all()
    context = {
        'objects': objects,
    }
    return render(request, 'users/map.html', context)


@login_required
def profile(request):
    """Профиль пользователя"""
    # Получаем все сессии пользователя
    user_sessions = Session_History.objects.filter(ID_User=request.user).order_by('-login_time')[:10]

    # Подсчет сессий за последний месяц
    last_month = datetime.now() - timedelta(days=30)
    session_count = Session_History.objects.filter(
        ID_User=request.user,
        login_time__gte=last_month
    ).count()

    # Подсчет объектов пользователя
    user_objects_count = Objects.objects.filter(ID_User=request.user).count()

    # Общая статистика системы
    total_objects_count = Objects.objects.count()

    # Используем встроенную модель User вместо Users
    from django.contrib.auth.models import User
    active_users_count = User.objects.filter(is_active=True).count()

    regions_count = Regions.objects.count()

    context = {
        'user': request.user,
        'recent_sessions': user_sessions,
        'session_count': session_count,
        'user_objects_count': user_objects_count,
        'total_objects_count': total_objects_count,
        'active_users_count': active_users_count,
        'regions_count': regions_count,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        user = request.user

        # Обновляем основные поля
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')

        # Сохраняем изменения
        user.save()

        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    return render(request, 'users/edit_profile.html')


def object_list(request):
    """Список объектов"""
    objects = Objects.objects.all()
    context = {
        'objects': objects,
    }
    return render(request, 'users/object_list.html', context)