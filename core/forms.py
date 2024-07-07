from django import forms
from .models import CheckinIndividual, CheckinEmpresa, Quarto, Hospede, Empresa

class CheckinIndividualForm(forms.ModelForm):
    selected_hospede_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    acompanhantes = forms.CharField(widget=forms.Textarea, required=False)
    hospedes_secundarios = forms.ModelMultipleChoiceField(queryset=Hospede.objects.filter(empresa=None), required=False)

    class Meta:
        model = CheckinIndividual
        fields = ['quarto', 'data_checkin', 'data_checkout', 'diaria', 'num_dias', 'companhia', 'motivo_viagem', 'acompanhantes']
        widgets = {
            'data_checkin': forms.DateInput(attrs={'type': 'date'}),
            'data_checkout': forms.DateInput(attrs={'type': 'date'}),
        }

class CheckinEmpresaForm(forms.ModelForm):
    selected_empresa_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    selected_hospede_empresa_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    acompanhantes = forms.CharField(widget=forms.Textarea, required=False)
    hospedes_secundarios = forms.ModelMultipleChoiceField(queryset=Hospede.objects.exclude(empresa=None), required=False)

    class Meta:
        model = CheckinEmpresa
        fields = ['quarto', 'data_checkin', 'data_checkout', 'diaria', 'num_dias', 'companhia', 'motivo_viagem', 'acompanhantes']
        widgets = {
            'data_checkin': forms.DateInput(attrs={'type': 'date'}),
            'data_checkout': forms.DateInput(attrs={'type': 'date'}),
        }

class HospedeForm(forms.ModelForm):
    class Meta:
        model = Hospede
        fields = ['nome_completo', 'cpf', 'email', 'telefone', 'endereco', 'empresa']

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome_empresa', 'cnpj', 'telefone', 'endereco']


class FinanceiroForm(forms.Form):
    data_inicial = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    data_final = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

