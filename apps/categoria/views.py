from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from apps.categoria.models import Categoria


class CategoriaList(ListView):
    model = Categoria

class CategoriaCreate(CreateView):
    model = Categoria
    fields = ['nome', 'descricao', 'tipo', 'status']

    def form_valid(self, form):
        form.save(self)
        return super(CategoriaCreate, self).form_valid(form)


class CategoriaUpdate(UpdateView):
    model = Categoria
    fields = ['nome', 'descricao', 'tipo', 'status']


class CategoriaDelete(DeleteView):
    model = Categoria
    success_url = reverse_lazy('list_categoria')


def DeniedDeleteCategoria(request):
    t = loader.get_template('categoria_denied_delete.html')
    c = {'foo': 'bar'}
    return HttpResponse(t.render(c, request))
