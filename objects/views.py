from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Objects, Regions, Session_History  # Добавлены все модели

@login_required
def object_list(request):
    """Список всех объектов"""
    objects = Objects.objects.select_related('ID_Region').all()
    return render(request, 'objects/object_list.html', {'objects': objects})

@login_required
def object_detail(request, object_id):
    """Детальная информация об объекте"""
    # Используем правильное имя поля - скорее всего 'id' или 'pk'
    obj = get_object_or_404(Objects, id=object_id)  # или pk=object_id
    return render(request, 'objects/object_detail.html', {'object': obj})

@login_required
def region_list(request):
    """Список регионов"""
    regions = Regions.objects.all()
    return render(request, 'objects/region_list.html', {'regions': regions})

@login_required
def session_history(request):
    """История сессий"""
    sessions = Session_History.objects.select_related('ID_User', 'ID_Object').all()
    return render(request, 'objects/session_history.html', {'sessions': sessions})