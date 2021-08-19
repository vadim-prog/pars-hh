from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .hh_api import *
from .models import *

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]

def index(request):

    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            # print(form.cleaned_data['vac_input'])
            res = Results(form.cleaned_data['vac_input'], form.cleaned_data['reg_input'])
            res_request = res.parsing()

            if len(res_request) != 0:
                for vac in range(0, len(res_request)):
                    print(res_request[vac].vacancy)
            return redirect('home')
            #return render(request, 'vacancy/index.html', {'form': form, 'menu': menu, 'title': 'HH_Parsing'})
    else:
        form = AddPostForm()

    return render(request, 'vacancy/index.html', {'form': form, 'menu': menu, 'title': 'HH_Parsing'})


def results(request):
    context = {
        'menu': menu,
        'title': 'HH_Parsing',
        # 'cat_selected': 0,
    }
    return render(request, 'vacancy/results.html', context=context)


def contact(request):
    context = {
        'menu': menu,
        'title': 'HH_Parsing',
        # 'cat_selected': 0,
    }
    return render(request, 'vacancy/contact.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'HH_Parsing',
        # 'cat_selected': 0,
    }
    return render(request, 'vacancy/about.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
