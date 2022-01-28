from django.urls import path
from apps.relatorio.views import tela_relatorios

urlpatterns = [
   # path('balancete_analitico/', relatorio_analitico_pdf.as_view(), name='balancete_analitico_pdf'),
   # path('balancete_sintetico/', relatorio_sintetico_pdf.as_view(), name='balancete_sintetico_pdf'),
   path('tela_relatorios/', tela_relatorios, name='tela_relatorios'),
]
