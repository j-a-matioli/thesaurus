from django import forms
from apps.movimento.models import Movimento

class DateInput(forms.DateInput):
    input_type = 'date'


class MovimentoForm(forms.ModelForm):

    def __int__(self):
        self.request.session['ano_corrente'] = self.year
        self.request.session['mes_corrente'] = self.month

    class Meta:
        model = Movimento
        fields = {'conta', 'data', 'valor', 'observ'}
        exclude = ['id']
        widget = {
            'data': DateInput(attrs={'placeholder': 'Data da transação!',
                                         'id': 'id_data'})
        }
        
    def clean(self):
        cleaned_data = super(MovimentoForm, self).clean()
        data = cleaned_data.get("data")

        if data :
            print('Cleaned the data: MES = ',data.month)
            if data.month != self.request.session['ano_corrente']:
                raise forms.ValidationError("Data fora do mês de movimento!")
        return cleaned_data
