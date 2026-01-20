from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

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
    user_sessions = Session_History.objects.filter(ID_User=request.user)

    context = {
        'user_sessions': user_sessions,
        'sessions_count': user_sessions.count(),
    }
    return render(request, 'users/profile.html', context)

def object_list(request):
    """Список объектов"""
    objects = Objects.objects.all()
    context = {
        'objects': objects,
    }
    return render(request, 'users/object_list.html', context)