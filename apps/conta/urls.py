from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.conta.views import ContaList, ContaCreate, ContaUpdate, ContaDelete

urlpatterns = [
    path('', ContaList.as_view(), name='list_conta'),
    path('create/', login_required(ContaCreate.as_view()), name='create_conta'),
    path('update/<int:pk>', login_required(ContaUpdate.as_view()), name='update_conta'),
    path('delete/<int:pk>', login_required(ContaDelete.as_view()), name='delete_conta'),
]
