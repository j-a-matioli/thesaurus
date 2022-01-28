from django import forms
from django.http import HttpResponse

from apps.movimento.models import Movimento


class TelaRelatoriosForm(forms.Form):
    mes_corrente = forms.IntegerField(help_text="Mês de competência.", initial='')
    ano_corrente = forms.IntegerField(help_text="Ano de competência.", initial='')

    def clean(self):
        super().clean()
        _ano = self.cleaned_data.get("ano_corrente")
        _mes = self.cleaned_data.get("mes_corrente")
        isMovto = Movimento.objects.filter(data__year=_ano).filter(data__month=_mes)

        if isMovto.count() == 0:
             raise forms.ValidationError("Nenhum registro encontrado!")

        return HttpResponse(_ano)
