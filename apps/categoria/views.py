from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.categoria.models import Categoria
from django.urls import reverse_lazy
from django.template import loader


class CategoriaList(ListView):
    model = Categoria

class CategoriaCreate(CreateView):
    model = Categoria
    fields = ['nome','descricao','tipo','status']


    def form_valid(self, form):
        form.save(self)
        return super(CategoriaCreate,self).form_valid(form)

class CategoriaUpdate(UpdateView):
    model = Categoria
    fields = ['nome','descricao','tipo','status']


class CategoriaDelete(DeleteView):
    model = Categoria

    def delete(self,*args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('list_categoria')
        fail_url = reverse_lazy('denied_delete')
        if self.object.conta_set.exists():
            return HttpResponseRedirect(fail_url)

        self.object.delete()
        return HttpResponseRedirect(success_url)


def DeniedDeleteCategoria(request):
    t = loader.get_template('categoria/categoria_denied_delete.html')
    c = {'foo': 'bar'}
    return HttpResponse(t.render(c, request))
