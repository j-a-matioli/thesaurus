from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.categoria.views import CategoriaList, CategoriaCreate, CategoriaUpdate, CategoriaDelete,DeniedDeleteCategoria

urlpatterns = [
    path('', CategoriaList.as_view(), name='list_categoria'),
    path('denied/', DeniedDeleteCategoria, name='denied_delete'),
    path('create/',  login_required(CategoriaCreate.as_view()), name='create_categoria'),
    path('update/<int:pk>',  login_required(CategoriaUpdate.as_view()), name='update_categoria'),
    path('delete/<int:pk>',  login_required(CategoriaDelete.as_view()), name='delete_categoria'),
]
