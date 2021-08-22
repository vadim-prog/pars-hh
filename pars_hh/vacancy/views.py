from django.http import HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from .hh_api import *
from .models import *
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]
'''
def get_context_data(self, **kwargs):
        context = super(PieceCreate, self).get_context_data(**kwargs)
        return context['id']

    def get_success_url(self):
        return reverse_lazy('pieceinstance-create', kwargs={'pk': self.get_context_data()})
'''

class Search(CreateView):
    form_class = AddSearchForm
    template_name = 'vacancy/index.html'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HH_Parsing'
        context['menu'] = menu
        context['res_request'] = 0
        return context

    def get_success_url(self):
        res = Results(self.object.input_vacancy, self.object.city, self.object.id)
        res.parsing()
        return reverse_lazy('results', kwargs={'pk': self.object.id})


class ResultsView(ListView):
    model = Output_data
    form_class = AddSearchForm
    template_name = 'vacancy/results.html'
    context_object_name = 'res_request'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HH_Parsing'
        context['menu'] = menu
        return context

    def get_queryset(self):
        return Output_data.objects.filter(input_vac_id = self.kwargs['pk'])


    #wu = Output_data.objects.get(id=request.POST.id)
    #print(wu)
    #res = Results(form.cleaned_data['input_vacancy'], form.cleaned_data['city'], form.save().pk)
#   res_request = res.parsing()


def get(self, request, pk):
    print(request.GET[pk]) # print all url params

'''

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'HH_Parsing'
        return context

    def get_queryset(self):
        return Output_data.objects.filter(input_vac_id)
        
'''
#def index(request):
#
#   if request.method == 'POST':
#        form = AddSearchForm(request.POST)
#       if form.is_valid():
#          form.save()
#            res = Results(form.cleaned_data['input_vacancy'], form.cleaned_data['city'], form.save().pk)
#            res_request = res.parsing()
#    else:
#        res_request = []
#        form = AddSearchForm()

#    return render(request, 'vacancy/index.html', {'res_request': res_request, 'form': form, 'menu': menu, 'title': 'HH_Parsing'})


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
