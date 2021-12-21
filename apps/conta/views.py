from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.conta.models import Conta
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

class ContaList(ListView):
    model = Conta


class ContaCreate(CreateView):
    model = Conta
    fields = ['nome','descricao','categoria','status']

    def form_valid(self, form):
        form.save(self)
        return super(ContaCreate,self).form_valid(form)

class ContaUpdate(UpdateView):
    model = Conta
    fields = ['nome','descricao','categoria','status']


class ContaDelete(DeleteView):
    model = Conta
    success_url = reverse_lazy('list_conta')




