from django.urls import path
from apps.movimento.views import MovimentoCreate,MovimentoList, MovimentoUpdate, MovimentoDelete

urlpatterns = [
    path('', MovimentoList.as_view(), name="list_movimento"),
    path('novo/', MovimentoCreate.as_view(), name="create_movimento"),
    path('update/<int:pk>', MovimentoUpdate.as_view(), name='update_movimento'),
    path('delete/<int:pk>', MovimentoDelete.as_view(), name='delete_movimento'),
]
