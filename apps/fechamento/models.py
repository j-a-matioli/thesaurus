from django.db import models
from django.urls import reverse
from datetime import date, datetime

FECHADO_CHOICES = [
    (True, 'Fechado'),
    (False, 'Aberto'),
]

class Fechamento(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.DateTimeField(null=False)
    saldo_anterior = models.DecimalField(default=0.0,decimal_places=2,max_digits=13)
    entradas = models.DecimalField(default=0.0,decimal_places=2,max_digits=13)
    saidas = models.DecimalField(default=0.0,decimal_places=2,max_digits=13)
    saldo = models.DecimalField(default=0.0,decimal_places=2,max_digits=13)
    fechado = models.BooleanField(default=False, choices=FECHADO_CHOICES)

    managed=True

    class Meta:
        # unique_together = (('ano', 'mes'),)        
        ordering = ['data',]

    def __str__(self):
        return self.data.month.__str__()+"/"+self.data.year.__str__()

    def get_absolute_url(self):
        return reverse('list_fechamento')

    def getSaldoAtual(self):
        saldo_atual = None
        saldo_atual = self.saldo_anterior+(self.entradas-self.saidas)
        self.saldo=saldo_atual
        return saldo_atual

    def updateSaldoAtual(self):
        Fechamento.objects.all().update(saldo=(self.saldo_anterior+(self.entradas-self.saidas)))
