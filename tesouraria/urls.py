from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('authenticate/',include('apps.authenticate.urls')),
    path('',include('apps.core.urls')),
    path('categoria/', include('apps.categoria.urls')),
    path('conta/', include('apps.conta.urls')),
    path('movimento/', include('apps.movimento.urls')),
    path('fechamento/', include('apps.fechamento.urls')),
    path('relatorio/', include('apps.relatorio.urls')),
    path('admin/', admin.site.urls),
]
