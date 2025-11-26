from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Object

class ObjectListView(ListView):
    model = Object
    template_name = 'objects/object_list.html'
    context_object_name = 'objects'
    paginate_by = 10

class ObjectDetailView(DetailView):
    model = Object
    template_name = 'objects/object_detail.html'
    context_object_name = 'object'