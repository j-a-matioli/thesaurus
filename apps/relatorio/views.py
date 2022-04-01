from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.datetime_safe import datetime
from weasyprint import HTML

from apps.movimento.models import Movimento
from apps.relatorio.forms import TelaRelatoriosForm


def bal_analitico_pdf(_mes, _ano):
    model = Movimento
    template_name = 'relatorio/relatorio_analitico_pdf.html'
    pdf_dest_name = 'balancete_analitico.pdf'
    ano_corrente = _ano
    mes_corrente = _mes
    context = {}

    dataSet = model.objects.filter(data__year=ano_corrente). \
        filter(data__month=mes_corrente). \
        order_by('data', 'conta__categoria', 'conta')

    setReceita = model.objects.filter(conta__categoria__tipo=1).filter(data__year=ano_corrente).filter(
        data__month=mes_corrente)

    setDespesa = model.objects.filter(conta__categoria__tipo=2).filter(data__year=ano_corrente).filter(
        data__month=mes_corrente)

    totalReceita = setReceita.aggregate(Sum('valor'))
    totalDespesa = setDespesa.aggregate(Sum('valor'))
    totalSaldo = setReceita.aggregate(Sum('valor')).get('valor__sum') + setDespesa.aggregate(Sum('valor')).get(
        'valor__sum')

    sumario = dataSet.values('conta__categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('conta__categoria__nome')

    # context['lancamentos'] = dataSet
    context['nreg'] = dataSet.count()
    context['dsReceita'] = setReceita
    context['totalReceita'] = totalReceita
    context['dsDespesa'] = setDespesa
    context['totalDespesa'] = totalDespesa
    context['totalSaldo'] = totalSaldo
    context['sumario'] = sumario
    context['mes_corrente'] = mes_corrente
    context['ano_corrente'] = ano_corrente
    context['data_emissao'] = datetime.now()

    html_string = render_to_string(template_name, context)
    html = HTML(string=html_string)
    html.write_pdf(target=pdf_dest_name);
    fs = FileSystemStorage()
    with fs.open(pdf_dest_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balancete_analitico.pdf"'

    return response


def bal_sintetico_pdf(_mes, _ano):
    model = Movimento
    template_name = 'relatorio/balancete_sintetico_pdf.html'
    pdf_dest_name = 'balancete_sintetico.pdf'
    ano_corrente = _ano
    mes_corrente = _mes
    context = {}

    setReceita = model.objects.filter(data__year=ano_corrente) \
        .filter(data__month=mes_corrente) \
        .filter(conta__categoria__tipo=1)

    sumarioReceita = setReceita.values('conta__categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('conta__categoria__nome')

    setDespesa = model.objects.filter(data__year=ano_corrente).filter(
        data__month=mes_corrente).filter(conta__categoria__tipo=2)

    sumarioDespesa = setDespesa.values('conta__categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('conta__categoria__nome')

    totalReceita = setReceita.aggregate(Sum('valor'))
    totalDespesa = setDespesa.aggregate(Sum('valor'))


    context['dsReceita'] = sumarioReceita
    context['totalReceita'] = totalReceita
    context['dsDespesa'] = sumarioDespesa
    context['totalDespesa'] = totalDespesa
    context['mes_corrente'] = mes_corrente
    context['ano_corrente'] = ano_corrente
    context['data_emissao'] = datetime.now()

    html_string = render_to_string(template_name, context)
    html = HTML(string=html_string)
    html.write_pdf(target=pdf_dest_name);
    fs = FileSystemStorage()
    with fs.open(pdf_dest_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balancete_sintetico.pdf"'

    return response


def bal_sintetico_pdf_old(_mes, _ano):
    model = Movimento
    template_name = 'relatorio/balancete_sintetico_pdf.html'
    pdf_dest_name = 'balancete_sintetico.pdf'
    ano_corrente = _ano
    mes_corrente = _mes
    context={};

    # obtem os dados para o relatorio
    setAll = model.objects.filter(data__year=ano_corrente). \
        filter(data__month=mes_corrente). \
        order_by('data', 'conta__categoria', 'conta')

    sumario = setAll.values('conta__categoria__nome') \
        .annotate(total=Sum('valor')) \
        .order_by('conta__categoria__nome')

    context['sumario'] = sumario
    context['mes_corrente'] = mes_corrente
    context['ano_corrente'] = ano_corrente
    context['perseguida'] = 'Hoje capturei a perseguida! ;)'
    context['data_emissao'] = datetime.now()

    html_string = render_to_string(template_name, context)
    html = HTML(string=html_string)
    html.write_pdf(target=pdf_dest_name);

    fs = FileSystemStorage()
    with fs.open(pdf_dest_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="balancete_sintetico.pdf"'

    return response

def tela_relatorios(request):
    if request.method=='POST':
        form = TelaRelatoriosForm(request.POST or None)
        if form.is_valid():
            _ano = request.POST.get('ano_corrente')
            _mes = request.POST.get('mes_corrente')
            if 'btn_balancete_analitico' in request.POST:
                return bal_analitico_pdf(_mes, _ano)
            if 'btn_balancete_sintetico' in request.POST:
                return bal_sintetico_pdf(_mes, _ano)
    else:
        form = TelaRelatoriosForm()

    context = {'form':form}
    return render(request, 'relatorio/tela_relatorios.html', context)
