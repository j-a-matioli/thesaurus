from django.urls import path, include

from apps.fechamento.views import FechamentoList, FechamentoCreate, FechamentoUpdate, FechamentoDelete, RenovaAssinatura

urlpatterns = [
    path('', FechamentoList.as_view(), name='list_fechamento'),
    path('create', FechamentoCreate.as_view(), name='create_fechamento'),
    path('<int:pk>/renovar', RenovaAssinatura, name='renova_assinatura'),
    path('update/<int:pk>', FechamentoUpdate.as_view(),name='update_fechamento'),
    path('delete/<int:pk>', FechamentoDelete.as_view(), name='delete_fechamento'),
]
