from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count
from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404
from objects.models import Objects

# Импортируем модели из objects приложения
from objects.models import Objects, Regions, Session_History
# Импортируем кастомную модель Users из текущего приложения main
from .models import Users


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
    try:
        objects = Objects.objects.select_related('ID_Region').all()

        # Логируем данные для отладки
        print(f"Найдено объектов: {objects.count()}")
        for obj in objects:
            print(f"Объект: {obj.Name_Object}, Координаты: {obj.Coordinates}")

    except Exception as e:
        print(f"Ошибка при получении объектов: {e}")
        objects = []

    context = {
        'objects': objects,
    }
    return render(request, 'users/map.html', context)

@login_required
def profile(request):
    """Профиль пользователя"""
    # Получаем все сессии - уберем фильтр по пользователю, так как в Session_History нет связи с Users
    recent_sessions = Session_History.objects.all().order_by('-Date', '-Time')[:10]

    # Подсчет сессий за последний месяц - также убираем фильтр по пользователю
    last_month = datetime.now() - timedelta(days=30)
    session_count = Session_History.objects.filter(
        Date__gte=last_month.date()
    ).count()

    # Подсчет объектов пользователя - убираем, так как в Objects нет связи с Users
    user_objects_count = 0  # Objects.objects.filter(ID_User=request.user).count()

    # Общая статистика системы
    total_objects_count = Objects.objects.count()
    active_users_count = Users.objects.filter(is_active=True).count()
    regions_count = Regions.objects.count()

    context = {
        'user': request.user,
        'recent_sessions': recent_sessions,
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

        # Обновляем основные поля кастомной модели Users
        user.Name = request.POST.get('first_name', '')
        user.Surname = request.POST.get('last_name', '')
        user.Patronymic = request.POST.get('patronymic', '')
        user.email = request.POST.get('email', '')

        # Сохраняем изменения
        user.save()

        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    return render(request, 'users/edit_profile.html')


def object_list(request):
    """Список объектов"""
    try:
        objects = Objects.objects.all()
    except Exception as e:
        objects = []

    context = {
        'objects': objects,
    }
    return render(request, 'users/object_list.html', context)

def object_detail(request, pk):
    """Детальная страница объекта"""
    obj = get_object_or_404(Objects, pk=pk)
    context = {
        'object': obj,
    }
    return render(request, 'users/object_detail.html', context)


def api_objects(request):
    objects = Objects.objects.all().values(
        'ID_Object', 'Name_Object', 'ID_Region__Name_Region',
        'Perimeter', 'Type_Of_Fence', 'Coordinates'
    )
    objects_list = list(objects)
    return Objects(objects_list, safe=False)