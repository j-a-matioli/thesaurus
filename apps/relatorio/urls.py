from django.urls import path
from apps.relatorio.views import relatorio_sintetico_pdf

urlpatterns = [
   path('', relatorio_sintetico_pdf.as_view(), name='relatorio_sintetico_pdf'),
]
