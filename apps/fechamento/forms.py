from django import forms
from django.utils.translation import gettext_lazy as _
from apps.fechamento.models import Fechamento
from django import forms


class FechamentoForm(forms.ModelForm):
         
     # def __init__(self, *args, **kwargs):
     #      super(FechamentoForm, self).__init__(*args, **kwargs)
     #      self.fields['saldo_anterior'].widget.attrs['readonly'] = True
          
     class Meta:
          model = Fechamento
          fields = '__all__'
          exclude = ('id', 'data', 'saldo')
          
         
        
