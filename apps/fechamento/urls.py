from django.urls import path, include

from apps.fechamento.views import FechamentoCriar,FechamentoEncerrar, FechamentoList,  FechamentoDelete, FechamentoRefresh, atualizar

urlpatterns = [
    path('', FechamentoList.as_view(), name='list_fechamento'),
    path('create', FechamentoCriar, name='create_fechamento'),
    path('refresh/<int:pk>', FechamentoRefresh,name='refresh_fechamento'),
    path('update/<int:pk>', atualizar,name='update_fechamento'),
    path('delete/<int:pk>', FechamentoDelete.as_view(), name='delete_fechamento'),
    path('encerrar/<int:pk>',FechamentoEncerrar, name='encerrar_fechamento' ),
]
