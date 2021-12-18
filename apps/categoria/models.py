from django.db import models
from django.urls import reverse

from apps import conta

TIPO_CHOICES = [
    (1, 'Receita'),
    (2, 'Despesa'),
]
STATUS_CHOICES = [
    (True, 'Ativa'),
    (False, 'Inativa'),
]

class Categoria(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome =models.CharField(max_length=50, unique=True, db_index=True)
    descricao = models.CharField(max_length=255, null=False)
    tipo = models.PositiveSmallIntegerField(default=1, choices=TIPO_CHOICES)
    status = models.BooleanField(default=True, choices=STATUS_CHOICES)

    class Metta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('categoria/list_categoria')



