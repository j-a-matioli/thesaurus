from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.utils.datetime_safe import datetime
from apps.movimento.models import Movimento
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string, get_template
from weasyprint import HTML
from django.db.models import Sum
from django.views.generic import TemplateView
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from apps.relatorio.forms import TelaRelatoriosForm
import tempfile

class relatorio_analitico_pdf(TemplateView):
    model = Movimento
    fields = ['conta', 'data', 'documento' , 'valor', 'observ']
    template_name = 'relatorio/relatorio_analitico_pdf.html'
    ordering = ['-data']
    agora = datetime.now()

    def get(self, request):
        contexto = self.get_context_data()
        if contexto:
            html_string = render_to_string(self.template_name, contexto)
            html = HTML(string=html_string)
            html.write_pdf(target='relatorio_analitico.pdf');
            fs = FileSystemStorage()
            with fs.open('relatorio_analitico.pdf') as pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="relatorio_analitico.pdf"'
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtro_mes = self.request.POST.get('mes_corrente')
        filtro_ano = self.request.POST.get('ano_corrente')

        setAll = Movimento.objects.filter(data__year=filtro_ano).\
            filter(data__month=filtro_mes).\
            order_by('data','conta__categoria','conta')
        if setAll.count()>0:
            setReceita = Movimento.objects.filter(conta__categoria__tipo=1).filter(data__year=filtro_ano).filter(
                data__month=filtro_mes)

            setDespesa = Movimento.objects.filter(conta__categoria__tipo=2).filter(data__year=filtro_ano).filter(
                data__month=filtro_mes)

            totalReceita = setReceita.aggregate(Sum('valor'))
            totalDespesa = setDespesa.aggregate(Sum('valor'))
            totalSaldo = setReceita.aggregate(Sum('valor')).get('valor__sum') + setDespesa.aggregate(Sum('valor')).get('valor__sum')

            sumario = setAll.values('conta__categoria__nome')\
                .annotate(total=Sum('valor'))\
                .order_by('conta__categoria__nome')

            context['lancamentos']=setAll
            context['nreg'] = setAll.count()
            context['totalReceita'] = totalReceita
            context['totalDespesa'] = totalDespesa
            context['totalSaldo'] = totalSaldo
            context['sumario'] = sumario
            context['mes'] = filtro_mes
            context['ano'] = filtro_ano
            context['data_emissao'] = self.agora
            context['dados'] = setAll #RelatorioSinteticoFilter(self.request.GET, queryset=setAll)

        return context

def bal_analitico_pdf(_mes, _ano):
    template_name = 'relatorio/relatorio_analitico_pdf.html'
    ano_corrente = _ano
    mes_corrente = _mes
    context = {}

    setAll = Movimento.objects.filter(data__year=ano_corrente). \
        filter(data__month=mes_corrente). \
        order_by('data', 'conta__categoria', 'conta')

    setReceita = Movimento.objects.filter(conta__categoria__tipo=1).filter(data__year=ano_corrente).filter(
        data__month=mes_corrente)

    setDespesa = Movimento.objects.filter(conta__categoria__tipo=2).filter(data__year=ano_corrente).filter(
        data__month=mes_corrente)

    totalReceita = setReceita.aggregate(Sum('valor'))
    totalDespesa = setDespesa.aggregate(Sum('valor'))
    totalSaldo = setReceita.aggregate(Sum('valor')).get('valor__sum') + setDespesa.aggregate(Sum('valor')).get(
        'valor__sum')

    sumario = setAll.values('conta__categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('conta__categoria__nome')

    context['lancamentos'] = setAll
    context['nreg'] = setAll.count()
    context['totalReceita'] = totalReceita
    context['totalDespesa'] = totalDespesa
    context['totalSaldo'] = totalSaldo
    context['sumario'] = sumario
    context['mes'] = mes_corrente
    context['ano'] = ano_corrente
    context['data_emissao'] = datetime.now()
    context['dados'] = setAll  # RelatorioSinteticoFilter(self.request.GET, queryset=setAll)

    html_string = render_to_string(template_name, context)
    html = HTML(string=html_string)
    html.write_pdf(target='relatorio_analitico.pdf');
    fs = FileSystemStorage()
    with fs.open('relatorio_analitico.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_analitico.pdf"'

    return response


def bal_sintetico_pdf(_mes, _ano):
    template_name = 'relatorio/relatorio_sintetico_pdf.html'

    # obtem os dados para o relatorio
    setAll = Movimento.objects.filter(data__year=_ano). \
        filter(data__month=_mes). \
        order_by('data', 'conta__categoria', 'conta')

    context = {}
    sumario = setAll.values('conta__categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('conta__categoria__nome')

    context['sumario'] = sumario
    context['mes'] = _mes
    context['ano'] = _ano
    context['data_emissao'] = datetime.now()

    html_string = render_to_string(template_name, context)
    html = HTML(string=html_string)
    html.write_pdf(target='relatorio_sintetico.pdf');

    fs = FileSystemStorage()
    with fs.open('relatorio_sitnetico.pdf') as output:
        response = HttpResponse(output, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_sintetico.pdf"'

    return response

def tela_relatorios(request):
    _ano = None
    _mes = None
    _btnAnalitico=False
    _btnSintetico=False

    if request.method=='POST':
        form = TelaRelatoriosForm(request.POST or None)
        if form.is_valid():
            _ano = request.POST.get('ano_corrente')
            _mes = request.POST.get('mes_corrente')
            if 'btn_balancete_analitico' in request.POST:
                _btnAnalitico=True
            if 'btn_balancete_sintetico' in request.POST:
                _btnSintetico = True

            isMovto = Movimento.objects.filter(data__year=_ano).filter(data__month=_mes)

            if isMovto.count()>0:
                if _btnSintetico==True:
                     return bal_sintetico_pdf(_mes, _ano)
                elif _btnAnalitico==True:
                     return bal_analitico_pdf(_mes, _ano)
    else:
        form = TelaRelatoriosForm()

    context = {'form':form}
    return render(request, 'relatorio/tela_relatorios.html', context)
