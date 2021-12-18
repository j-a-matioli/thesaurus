from django.urls import path, include

from apps.conta.views import ContaList, ContaCreate, ContaUpdate, ContaDelete

urlpatterns = [
    path('', ContaList.as_view(), name='list_conta'),
    path('create', ContaCreate.as_view(), name='create_conta'),
    path('update/<int:pk>', ContaUpdate.as_view(), name='update_conta'),
    path('delete/<int:pk>', ContaDelete.as_view(), name='delete_conta'),
]
