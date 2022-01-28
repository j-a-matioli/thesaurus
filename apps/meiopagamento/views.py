from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from apps.meiopagamento.models import MeioPagamento

class MeioPagamentoList(ListView):
    model = MeioPagamento


class MeiopagamentoCreate(CreateView):
    model = MeioPagamento
    fields = ['nome','descricao',]
    success_url = reverse_lazy("create_meiopagamento")

    def form_valid(self, form):
        form.save(self)
        return super(MeiopagamentoCreate,self).form_valid(form)

class MeiopagamentoUpdate(UpdateView):
    model = MeioPagamento
    fields = ['nome','descricao']


class MeiopagamentoDelete(DeleteView):
    model = MeioPagamento
    success_url = reverse_lazy('list_meiopagamento')
