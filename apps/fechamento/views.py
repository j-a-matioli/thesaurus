from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from decimal import Decimal
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.fechamento.forms import FechamentoForm
from apps.fechamento.models import Fechamento

class FechamentoList(ListView):
    model = Fechamento

class FechamentoCreate(CreateView):
    model = Fechamento
    ultimo = Fechamento.objects.last()
    if ultimo:
        str_data_ultimo = '01/' + ultimo.mes.__str__() + '/' + ultimo.ano.__str__()
        prx_data = ultimo.data + relativedelta(months=1)
    else:
        _mes = datetime.today().month.__str__()
        _ano = datetime.today().year.__str__()
        str_data_ultimo = '01/'+_mes+'/'+_ano
        data_ultimo = datetime.strptime(str_data_ultimo, '%d/%m/%Y').date()
        prx_data = data_ultimo + relativedelta(months=1)

    if ultimo:
        initial = {'id':ultimo.id,"mes": prx_data.month,'ano':prx_data.year, "data":prx_data.date(),
                   'saldo_anterior':(ultimo.saldo_anterior + (ultimo.entradas - ultimo.saidas)) }
    else:
        initial = {"data":prx_data.date()}

    fields = ['id','data','saldo_anterior']

    def form_valid(self, form):

        form.save(self)
        return super(FechamentoCreate,self).form_valid(form)

    # def form_valid(self, form):
    #     fecha = get_object_or_404(Fechamento, pk=self.kwargs['id'])
    #     form.instance.fechamento = fecha
    #     return super(FechamentoCreate, self).form_valid(form)


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
