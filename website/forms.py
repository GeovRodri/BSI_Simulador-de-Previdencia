from django import forms
from website.models import GENDER_CHOICES


class SimulacaoForm(forms.Form):
    nome = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    sexo = forms.ChoiceField(
        label='Sexo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=GENDER_CHOICES)

    cpf = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={'class': 'form-control mascara-cpfcnpj'}),
        max_length=14,
        min_length=14)

    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial='2000-01-01')

    data_inicial_contribuicao = forms.DateField(
        label='Data Inicial da Contribuição',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial='2000-01-01')

    data_ultima_contribuicao = forms.DateField(
        label='Data da ultima Contribuição',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial='2019-01-01')

    valor_contribuicao = forms.FloatField(
        label='Contribuição(R$/Ano)',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial="0.00")

    # valor_contribuicao = forms.CharField(widget=forms.HiddenInput())
