from django import forms
from .models import Checkin, Quarto, Hospede, Empresa


class CheckinForm(forms.ModelForm):
    tipo_hospede = forms.ChoiceField(choices=[('individual', 'Individual'), ('empresa', 'Empresa')], required=True)
    hospede_principal = forms.ModelChoiceField(queryset=Hospede.objects.filter(tipo_cliente='individual'), required=False)
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.all(), required=False)
    acompanhantes = forms.CharField(widget=forms.Textarea, required=False)
    hospedes_secundarios = forms.ModelMultipleChoiceField(queryset=Hospede.objects.filter(tipo_cliente='individual'), required=False)

    class Meta:
        model = Checkin
        fields = ['quarto', 'data_checkin', 'data_checkout', 'diaria', 'num_dias', 'companhia', 'motivo_viagem', 'acompanhantes']
class HospedeForm(forms.ModelForm):
    class Meta:
        model = Hospede
        fields = ['nome_completo', 'cpf', 'email', 'telefone', 'endereco', 'tipo_cliente', 'empresa']


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome_empresa', 'cnpj', 'telefone', 'endereco']


class FinanceiroForm(forms.Form):
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    data_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

