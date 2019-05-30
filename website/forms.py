from django import forms


class SimulacaoForm(forms.Form):
    name = forms.CharField(
        label='Nome',
        widget=forms.TextInput(attrs={'class': 'form-control'})),

    cpf = forms.CharField(
        label='CPF',
        widget=forms.TextInput(attrs={'class': 'form-control mascara-cpfcnpj'}),
        max_length=12)

    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial='2000-01-01')

    tempo_contribuicao = forms.IntegerField(
        label='Tempo de Contribuição',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        min_value=1)

    valor_contribuicao = forms.FloatField(
        label='Contribuição(R$/Mês)',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        initial="0.00")

