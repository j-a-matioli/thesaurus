from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import MeioPagamentoList,MeiopagamentoCreate, MeiopagamentoUpdate, MeiopagamentoDelete

urlpatterns = [
    path('', MeioPagamentoList.as_view(), name='list_meiopagamento'),
    path('create/', login_required(MeiopagamentoCreate.as_view()), name='create_meiopagamento'),
    path('update/<int:pk>', login_required(MeiopagamentoUpdate.as_view()), name='update_meiopagamento'),
    path('delete/<int:pk>', login_required(MeiopagamentoDelete.as_view()), name='delete_meiopagamento'),
]
