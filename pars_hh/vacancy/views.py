from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404


def index(request):
    return HttpResponse('<h1>Главная страница</h1>')


def contact(request):
    return HttpResponse("Обратная связь")


def about(request):
    return HttpResponse("О сайте")


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
