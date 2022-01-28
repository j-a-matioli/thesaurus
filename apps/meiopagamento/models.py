from django.db import models
from django.urls import reverse

STATUS_CHOICES = [
    (True, 'Ativa'),
    (False, 'Inativa'),
]

class MeioPagamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    nome =models.CharField(max_length=100, unique=True, db_index=True)
    descricao = models.CharField(max_length=255, null=False)

    class Metta:
        ordering = ('nome',)

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('list_meiopagamento')
