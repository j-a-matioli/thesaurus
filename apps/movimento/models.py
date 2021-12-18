from django.db import models
from django.db.models import Sum, Value
from apps.conta.models import Conta


class Movimento(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    conta = models.ForeignKey(Conta, on_delete=models.PROTECT)
    data = models.fields.DateField()
    valor = models.DecimalField(max_digits=13, decimal_places=2)
    observ = models.CharField(max_length=100, blank=True, null=False)

    class Meta:
        ordering = ('data','conta')
