from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Fix: Import from objects app instead of main
from objects.models import Objects, Regions, Session_History


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
    # Простая статистика для главной страницы
    total_objects = Objects.objects.count()
    total_regions = Regions.objects.count()
    total_sessions = Session_History.objects.count()

    context = {
        'total_objects': total_objects,
        'total_regions': total_regions,
        'total_sessions': total_sessions,
    }
    return render(request, 'users/home.html', context)


def map_view(request):
    objects = Objects.objects.all()
    context = {
        'objects': objects,
    }
    return render(request, 'users/map.html', context)


@login_required
def profile(request):
    # Простая страница профиля
    user_sessions = Session_History.objects.filter(ID_User=request.user)

    context = {
        'user_sessions': user_sessions,
        'sessions_count': user_sessions.count(),
    }
    return render(request, 'users/profile.html', context)