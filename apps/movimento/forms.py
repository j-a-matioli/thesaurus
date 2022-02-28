from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from crispy_forms.layout import Submit
from django import forms
from django.forms import DateInput

from apps.fechamento.models import Fechamento
from apps.movimento.models import Movimento
from apps.conta.models import Conta
from apps.meiopagamento.models import MeioPagamento

class MovimentoForm(forms.ModelForm):
    competencia = forms.ModelChoiceField(queryset=Fechamento)
    conta = forms.ModelChoiceField(queryset=Conta)
    data = forms.DateField(label='', help_text='', attrs={'id': 'id_data',  'class': 'form-control disabled', 'placeholder': 'Data do pagamento'})
    meiopagamento = forms.ModelChoiceField(queryset=MeioPagamento)
    documento = forms.TextInput(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nr. Documento'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request.session['ano_corrente'] = self.year
        self.request.session['mes_corrente'] = self.month

    class Meta:
        model = Movimento
        fields = '__all__'
        exclude = ['id']
        widgets = {
            'data':  {'date': DateInput(attrs={'class': 'datepicker'})}
        }

