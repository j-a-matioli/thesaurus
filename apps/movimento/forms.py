from django import forms
from apps.movimento.models import Movimento
from django.db.models import Sum

class MovimentoForm(forms.ModelForm):
    class Meta:
        # Modelo base
        model = Movimento
        fields =['conta','data','valor','observ']
        # Campos que não estarão no form
        exclude = [ 'id' ]

        widgets = {
            'data' : forms.SelectDateWidget,
            'observ' : forms.Textarea(attrs={'cols': 80, 'rows': 2}),
        }
