from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.movimento.forms import MovimentoForm
from apps.movimento.models import Movimento
from django.db.models import Sum, Value
from .filters import MovimentoFilter
from datetime import datetime

class MovimentoList(ListView):
    model = Movimento
    fields = ['conta', 'data', 'valor', 'observ']
    template_name = 'movimento/movimento_list.html'
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
        context['totalReceita'] = totalReceita
        context['totalDespesa'] = totalDespesa
        context['mes'] = filtro_mes
        context['ano'] = filtro_ano
        context['dados'] = MovimentoFilter(self.request.GET, queryset=setAll)
        return context

class MovimentoCreate(CreateView):
    template_name = 'movimento/movimento_form.html'
    model = Movimento
    form_class = MovimentoForm
    success_url = reverse_lazy("list_movimento")

class MovimentoUpdate(UpdateView):
    model = Movimento
    fields = ['conta','data','valor','observ']
    template_name = 'movimento/movimento_form.html'
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

