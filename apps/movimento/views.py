from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.fechamento.models import Fechamento
from apps.movimento.forms import MovimentoForm
from apps.movimento.models import Movimento
from django.db.models import Sum, Value
from .filters import MovimentoFilter
from datetime import datetime

class MovimentoList(ListView):
    model = Movimento
    fields = ['conta', 'data', 'valor', 'observ']
    template_name = 'list_movimento'
    ordering = ['-data']
    agora = datetime.now()
    year = agora.year.__str__()
    month = agora.month.__str__()
    
    def __int__(self):
        self.request.session['ano_corrente'] = self.year
        self.request.session['mes_corrente'] = self.month

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtro_mes = self.request.GET.get('mes_corrente')
        filtro_ano = self.request.GET.get('ano_corrente')

        if not filtro_mes:
            filtro_mes = self.request.session.get('mes_corrente')
        else:
            self.request.session['mes_corrente']=filtro_mes

        if not filtro_ano:
            filtro_ano = self.request.session.get('ano_corrente')
        else:
            self.request.session['ano_corrente']=filtro_ano

        setAll = Movimento.objects.filter(data__year=filtro_ano).filter(data__month=filtro_mes)
        setReceita = Movimento.objects.filter(conta__categoria__tipo=1).filter(data__year=filtro_ano).filter(
            data__month=filtro_mes)
        setDespesa = Movimento.objects.filter(conta__categoria__tipo=2).filter(data__year=filtro_ano).filter(
            data__month=filtro_mes)
        totalReceita = setReceita.aggregate(Sum('valor'))
        totalDespesa = setDespesa.aggregate(Sum('valor'))
        if totalReceita and totalDespesa:
            totalSaldo = setReceita.aggregate(Sum('valor')).get('valor__sum') + setDespesa.aggregate(Sum('valor')).get('valor__sum')
        else:
            totalSaldo = 0.0

        
        context['totalReceita'] = totalReceita
        context['totalDespesa'] = totalDespesa
        context['totalSaldo'] = totalSaldo
        context['mes'] = filtro_mes
        context['ano'] = filtro_ano
        if(setAll):
            context['dados'] = MovimentoFilter(self.request.GET, queryset=setAll)
        else:
            context['dados'] = None

        fechaData = Fechamento.objects.filter(data__month=filtro_mes, data__year=filtro_ano)
        if fechaData:
            context['fechado'] = fechaData[0].fechado
        else:
            context['fechado'] = False


        return context

class MovimentoCreate(CreateView):
    model = Movimento
    fields = ['conta','data','valor','observ']
    success_url = reverse_lazy("create_movimento")

    def form_valid(self, form):
        if form.instance.conta.categoria.tipo==2:
            form.instance.valor *= -1;
        form.save(self)
        return super(MovimentoCreate,self).form_valid(form)

class MovimentoUpdate(UpdateView):
    model = Movimento
    fields = ['conta','data','valor','observ']
    success_url = reverse_lazy("list_movimento")

class MovimentoDelete(DeleteView):
    model = Movimento
    success_url = reverse_lazy('list_movimento')

"""     def delete(self,*args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('list_movimento')
        self.object.delete()
        return HttpResponseRedirect(success_url)
 """

