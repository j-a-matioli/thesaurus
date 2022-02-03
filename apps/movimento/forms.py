from django import forms

from apps.fechamento.models import Fechamento
from apps.movimento.models import Movimento
from apps.conta.models import Conta
from apps.meiopagamento.models import MeioPagamento

class MovimentoForm(forms.ModelForm):
    competencia = forms.ModelChoiceField(queryset=Fechamento)
    conta = forms.ModelChoiceField(queryset=Conta)
    meiopagamento = forms.ModelChoiceField(queryset=MeioPagamento)
    documento = forms.TextInput(attrs={'placeholder':'Documento'})
    def __int__(self):
        self.request.session['ano_corrente'] = self.year
        self.request.session['mes_corrente'] = self.month

    class Meta:
        model = Movimento
        fields = {'conta', 'data', 'documento', 'valor', 'meiopagamento','observ'}
        exclude = ['id']

    def clean(self):
        cleaned_data = super(MovimentoForm, self).clean()
        data = cleaned_data.get("data")

        if data :
            print('Cleaned the data: MES = ',data.month)
            if data.month != self.request.session['ano_corrente']:
                raise forms.ValidationError("Data fora do mês de movimento!")
        return cleaned_data
