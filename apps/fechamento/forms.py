import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class FechamentoForm(forms.Form):
    data_renovacao = forms.DateField(widget=forms.widgets.DateInput(format="%m/%d/%Y"),help_text="Enter a date between now and 4 weeks (default 3).")
    def clean_data_renovacao(self):
        data = self.cleaned_data['data_renovacao']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida. Está no passado!'))

        # Check if a date is in the allowed range (+4 weeks from today).
        if data > datetime.date.today() + datetime.timedelta(days=90):
            raise ValidationError(_('Data inválida. Está a mais de 3 semanas a frente!'))

        # Remember to always return the cleaned data.
        return data
