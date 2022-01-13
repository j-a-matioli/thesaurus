from django.db.models import fields
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from decimal import Decimal
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from dateutil import relativedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, request
from django.urls import reverse

from apps.fechamento.forms import FechamentoForm
from apps.fechamento.models import Fechamento

class FechamentoList(ListView):
    model = Fechamento
    
def FechamentoEncerrar(request,pk):
    model = Fechamento
    registro = get_object_or_404(Fechamento, pk=pk)
    if registro and (request.method == "GET"):
        model.objects.filter(pk=pk).update(fechado=not registro.fechado, saldo=(registro.saldo_anterior+(registro.entradas-registro.saidas)))
    return HttpResponseRedirect(reverse('list_fechamento') )

def FechamentoCriar(request):
    model = Fechamento
    data = date.today()
    saldo_anterior = 0.0
    saldo = 0
    
    if Fechamento.objects.first():
        lastReg = model.objects.latest('data')
        data = lastReg.data + relativedelta.relativedelta(months=1, day=1)
        saldo_anterior = lastReg.saldo
        saldo = lastReg.saldo
        print(data, saldo_anterior,saldo)     
               
    newReg = Fechamento(data=data, saldo_anterior=saldo_anterior,saldo=saldo)
    newReg.save()
    
    return HttpResponseRedirect(reverse('list_fechamento') )

class FechamentoCreate(CreateView):
    model = Fechamento
    fields = ['id','data','saldo_anterior']

    class Meta:
        readonly = ['data', ]
    
    def form_valid(self, form):
        form.save(self)
        return super(FechamentoCreate,self).form_valid(form)




class FechamentoUpdate(UpdateView):
    model = Fechamento
    fields = ['id','data','saldo_anterior','entradas','saidas']

    def get_success_url(self, **kwargs):
        return reverse_lazy("list_fechamento")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saldo']=self.object.getSaldoAtual()
        return context

    def form_valid(self, form):
        _sldAnterior = form['saldo_anterior'].value()
        _entradas = form['entradas'].value()
        _saidas = form['saidas'].value()
        _saldo = Decimal(_sldAnterior) + (Decimal(_entradas) - Decimal(_saidas))
        form.save(self)
        return super(FechamentoUpdate,self).form_valid(form)


    success_url = reverse_lazy("list_fechamento")

class FechamentoDelete(DeleteView):
    model = Fechamento
    success_url = reverse_lazy('list_fechamento')

def RenovaAssinatura(request, pk):
    mes_fechamento = get_object_or_404(Fechamento, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = FechamentoForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            mes_fechamento.data = form.cleaned_data['data_renovacao']
            mes_fechamento.save()

            # redirect to a new URL:
            #reverse('detail', kwargs={'slug' : self.object.slug})
            return HttpResponseRedirect(reverse('list_fechamento') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.today() + timedelta(weeks=3)
        form = FechamentoForm(initial={'data_renovacao': proposed_renewal_date})

    context = {
        'form': form,
        'mes_fechamento': mes_fechamento,
    }

    return render(request, "fechamento/fechamento_renova.html", context)
