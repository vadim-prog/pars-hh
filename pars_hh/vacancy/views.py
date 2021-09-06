from django.http import HttpResponseNotFound, Http404, request, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .models import *
from django.views.generic import CreateView, ListView, TemplateView
from django.urls import reverse_lazy
from .tasks import res_pars


menu = [{'title': "Результаты", 'url_name': 'results'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]


class SearchView(CreateView):
    form_class = AddSearchForm
    template_name = 'vacancy/index.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HH_Parsing'
        context['menu'] = menu
        context['res_request'] = 0
        context['pk'] = None
        return context

    def get_success_url(self):
        res_pars.delay(self.object.input_vacancy, self.object.city, self.object.id)  # Запуск в селери
        return reverse_lazy('results', kwargs={'pk': self.object.id})


class ResultsView(ListView):
    paginate_by = 10
    model = Output_data
    template_name = 'vacancy/results.html'
    context_object_name = 'res_request'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HH_Parsing'
        context['menu'] = menu
        context['cur_vac'] = Search.objects.get(id=self.kwargs['pk']).input_vacancy
        context['cur_city'] = Search.objects.get(id=self.kwargs['pk']).city
        context['vac_found'] = len(Output_data.objects.filter(input_vac_id=self.kwargs['pk']))
        context['pk'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return Output_data.objects.filter(input_vac_id=self.kwargs['pk'])


def contact(request):
    context = {
        'menu': menu,
        'title': 'HH_Parsing',
    }
    return render(request, 'vacancy/contact.html', context=context)


def about(request):
    context = {
        'menu': menu,
        'title': 'HH_Parsing',
    }
    return render(request, 'vacancy/about.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
