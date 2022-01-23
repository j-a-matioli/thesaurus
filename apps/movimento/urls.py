from django.contrib.auth.decorators import login_required
from django.urls import path
from apps.movimento.views import MovimentoCreate,MovimentoList, MovimentoUpdate, MovimentoDelete

urlpatterns = [
    path('', MovimentoList.as_view(), name="list_movimento"),
    path('novo/', login_required(MovimentoCreate.as_view()), name="create_movimento"),
    path('update/<int:pk>', login_required(MovimentoUpdate.as_view()), name='update_movimento'),
    path('delete/<int:pk>', login_required(MovimentoDelete.as_view()), name='delete_movimento'),
]
