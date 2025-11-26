from django.shortcuts import render

def home(request):
    return render(request, 'main/home.html')

def map_view(request):
    try:
        from objects.models import Object
        objects = Object.objects.all()
        return render(request, 'main/map.html', {'objects': objects})
    except ImportError:
        # Если модель еще не создана, передаем пустой список
        return render(request, 'main/map.html', {'objects': []})