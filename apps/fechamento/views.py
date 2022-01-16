from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from decimal import Decimal
from datetime import date
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from dateutil.relativedelta import relativedelta

from apps.fechamento.forms import FechamentoForm
from apps.fechamento.models import Fechamento


class FechamentoList(ListView):
    model = Fechamento


def FechamentoEncerrar(request, pk):
    model = Fechamento
    registro = get_object_or_404(Fechamento, pk=pk)
    if registro and (request.method == "GET"):
        model.objects.filter(pk=pk).update(fechado=not registro.fechado, saldo=(
            registro.saldo_anterior+(registro.entradas-registro.saidas)))
    return HttpResponseRedirect(reverse('list_fechamento'))


def FechamentoCriar(request):
    data = date.today()
    saldo_anterior = 0.0
    saldo = 0

    if Fechamento.objects.count()>0:
        lastReg = Fechamento.objects.latest('data')
        data = lastReg.data + relativedelta(months=1, day=1)
        saldo_anterior = lastReg.saldo
        saldo = lastReg.saldo

    newReg = Fechamento()
    #newReg.id = 0
    newReg.data = data
    newReg.entradas=0.0
    newReg.saidas=0.0
    newReg.saldo_anterior = saldo_anterior
    newReg.saldo= saldo
    print("Novo : ",newReg)
    newReg.save()

    return HttpResponseRedirect(reverse('list_fechamento'))


class FechamentoCreate(CreateView):
    model = Fechamento
    fields = ['id', 'data', 'saldo_anterior']

    def form_valid(self, form):
        form.save(self)
        return super(FechamentoCreate, self).form_valid(form)


def atualizar(request, *args, **kwargs):
    model = Fechamento
    saldo_anterior = 0.0
    saldo = 0

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        periodo = Fechamento.objects.get(id=kwargs['pk'])
        form = FechamentoForm(request.POST, instance=periodo)

        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            post = form.save(commit=False)
            post.fechado = False
            post.saldo = post.saldo_anterior+(post.entradas - post.saidas)
            post.save()
            return HttpResponseRedirect(reverse('list_fechamento'))
    else:
        periodo = Fechamento.objects.get(pk=kwargs["pk"])
        form = FechamentoForm(instance=periodo)
        mydict = {
            'form': form
        }        
        return render(request, 'fechamento/fechamento_form.html', context=mydict)


class FechamentoUpdateCOPY(UpdateView):
    model = Fechamento
    fields = ['id', 'data', 'saldo_anterior', 'entradas', 'saidas']

    context = {}
    form = FechamentoForm(UpdateView.post or None)
    context['form'] = form

    def get_success_url(self, **kwargs):
        return reverse_lazy("list_fechamento")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saldo'] = self.object.getSaldoAtual()
        return context

    def form_valid(self, form):
        _sldAnterior = form['saldo_anterior'].value()
        _entradas = form['entradas'].value()
        _saidas = form['saidas'].value()
        _saldo = Decimal(_sldAnterior) + \
            (Decimal(_entradas) - Decimal(_saidas))
        form.save(self)
        return super(FechamentoForm, self).form_valid(form)

    success_url = reverse_lazy("list_fechamento")


class FechamentoDelete(DeleteView):
    model = Fechamento
    success_url = reverse_lazy('list_fechamento')
