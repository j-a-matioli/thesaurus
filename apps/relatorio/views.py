import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from apps.movimento.models import Movimento
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from datetime import datetime
from django.db.models import Sum
from .filters import RelatorioSinteticoFilter
from django.views.generic import ListView, TemplateView
from django.urls import reverse_lazy
import locale

class relatorio_sintetico_pdf(TemplateView):
    model = Movimento
    fields = ['conta', 'data', 'valor', 'observ']
    template_name = 'relatorio/relatorio_sintetico_pdf.html'
    ordering = ['-data']
    agora = datetime.now()
    year = agora.year.__str__()
    month = agora.month.__str__()

    def __int__(self):
        self.request.session['ano_corrente'] = self.year
        self.request.session['mes_corrente'] = self.month

    def get(self, request):
        contexto = self.get_context_data()
        html =  render_to_string(self.template_name,contexto)
        documento_html = HTML(string=html, base_url=request.build_absolute_uri())
        document = documento_html.render()
        if len(document.pages) > 1:
            for page in document.pages[1:]:
                str(page)
            pdf = document.write_pdf()
        else:
            pdf = document.write_pdf()

        fs = FileSystemStorage()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="rel_sintetico.pdf"'
        return response

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

        setAll = Movimento.objects.filter(data__year=filtro_ano).\
            filter(data__month=filtro_mes).\
            order_by('conta__categoria','data','conta')

        setReceita = Movimento.objects.filter(conta__categoria__tipo=1).filter(data__year=filtro_ano).filter(
            data__month=filtro_mes)
        setDespesa = Movimento.objects.filter(conta__categoria__tipo=2).filter(data__year=filtro_ano).filter(
            data__month=filtro_mes)
        totalReceita = setReceita.aggregate(Sum('valor'))
        totalDespesa = setDespesa.aggregate(Sum('valor'))
        totalSaldo = setReceita.aggregate(Sum('valor')).get('valor__sum') - setDespesa.aggregate(Sum('valor')).get('valor__sum')

        sumario = setAll.values('conta__categoria__nome')\
            .annotate(total=Sum('valor'))\
            .order_by('conta__categoria__nome')

        context['lancamentos']=setAll
        context['totalReceita'] = totalReceita
        context['totalDespesa'] = totalDespesa
        context['totalSaldo'] = totalSaldo
        context['sumario'] = sumario
        context['mes'] = filtro_mes
        context['ano'] = filtro_ano
        context['dados'] = RelatorioSinteticoFilter(self.request.GET, queryset=setAll)
        return context



def zrelatorio_sintetico_pdf(request):
    movimento = Movimento.objects.all()
    fields = ['conta', 'data', 'valor', 'observ']
    template_name = 'relatorio_sintetico_pdf.html'
    filename = 'rel_sintetico.pdf'
    documento_html=''
    ordering = ['-data']
    agora = datetime.now()
    year = agora.year.__str__()
    month = agora.month.__str__()

    context = {'lancamentos': movimento}

    html =  render_to_string(template_name,context)
    documento_html = HTML(string=html, base_url=request.build_absolute_uri())

    document = documento_html.render()
    if len(document.pages) > 1:
        for page in document.pages[1:]:
            str(page)
        pdf = document.write_pdf()
    else:
        pdf = document.write_pdf()

    fs = FileSystemStorage()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="rel_sintetico.pdf"'
    return response

def yrelatorio_sintetico_pdf(request):
    movimento = Movimento.objects.all().order_by('data').order_by('conta')

    # Rendered
    html_string = render_to_string('/rel_sintetico.html', {'movimento': movimento})
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    #response['Content-Disposition'] = 'inline; filename=rel_sintetico.pdf'
    response['Content-Disposition'] = 'attachment; filename="rel_sintetico.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.seek(0)
        output.write(result)
        output.flush()
        response.write(output.read())

    return response



def xrelatorio_sintetico_pdf(request):
    movimento = Movimento.objects.all().order_by('data').order_by('conta')

    # Rendered
    #html_string = render_to_string('/rel_sintetico.html', {'movimento': movimento})
    html_string = os.getcwd()
    html = HTML(string=html_string)
    result = html.write_pdf()

    # Creating http response
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=rel_sintetico.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output = open(output.name, 'rb')
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response
