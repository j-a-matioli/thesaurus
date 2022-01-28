from django import forms
from apps.meiopagamento.models import MeioPagamento

class MovimentoForm(forms.ModelForm):
    nome = forms.CharField(label='',help_text='',max_length=100, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Nome do meio de pagamento/recebimento'}))
    last_name = forms.CharField(label='',help_text='',max_length=50, widget=forms.Textarea(attrs={'class':'form-control','placeholder':'Descrição do meio de pagamento/recebimento','rows': 50, 'cols': 55}))

    class Meta:
        model = MeioPagamento
        fields = {'nome', 'descricao',}
        exclude = ['id']
