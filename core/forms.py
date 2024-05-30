from django import forms
from .models import Checkin, Quarto, Hospede


class CheckinForm(forms.ModelForm):
    class Meta:
        model = Checkin
        fields = [
            'hospede', 'quarto', 'data_checkin', 'data_checkout',
            'diaria', 'num_dias', 'companhia', 'motivo_viagem', 'numero_total_hospedes'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quarto'].queryset = Quarto.objects.filter(estado='livre')
        self.fields['hospede'].queryset = Hospede.objects.all()
        self.fields['data_checkin'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['data_checkout'].widget = forms.DateInput(attrs={'type': 'date'})