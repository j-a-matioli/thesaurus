from django.urls import path, include

from apps.categoria.views import CategoriaList, CategoriaCreate, CategoriaUpdate, CategoriaDelete,DeniedDeleteCategoria

urlpatterns = [
    path('', CategoriaList.as_view(), name='list_categoria'),
    path('denied/', DeniedDeleteCategoria, name='denied_delete'),
    path('create', CategoriaCreate.as_view(), name='create_categoria'),
    path('update/<int:pk>', CategoriaUpdate.as_view(), name='update_categoria'),
    path('delete/<int:pk>', CategoriaDelete.as_view(), name='delete_categoria'),

]
