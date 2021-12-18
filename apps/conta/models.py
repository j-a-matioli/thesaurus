from django.db import models
from django.urls import reverse
from apps.categoria.models import Categoria

STATUS_CHOICES = [
    (True, 'Ativa'),
    (False, 'Inativa'),
]

class Conta(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome =models.CharField(max_length=50, unique=True, db_index=True)
    descricao = models.CharField(max_length=255, null=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)

    class Metta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('list_conta')
