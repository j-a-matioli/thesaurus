from django.contrib.auth.decorators import login_required
from django.urls import path, include

from apps.fechamento.views import FechamentoCriar,FechamentoEncerrar, FechamentoList,  FechamentoDelete, FechamentoRefresh, atualizar

urlpatterns = [
    path('', FechamentoList.as_view(), name='list_fechamento'),
    path('create', login_required(FechamentoCriar), name='create_fechamento'),
    path('refresh/<int:pk>', login_required(FechamentoRefresh),name='refresh_fechamento'),
    path('update/<int:pk>', login_required(atualizar),name='update_fechamento'),
    path('delete/<int:pk>', login_required(FechamentoDelete.as_view()), name='delete_fechamento'),
    path('encerrar/<int:pk>',login_required(FechamentoEncerrar), name='encerrar_fechamento' ),
]
