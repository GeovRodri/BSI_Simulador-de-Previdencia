from django import forms
from website.models import GENDER_CHOICES


class SimulacaoForm(forms.Form):
    nome = forms.CharField()

    sexo = forms.ChoiceField(choices=GENDER_CHOICES)

    cpf = forms.CharField(max_length=14, min_length=14)

    nascimento = forms.DateField(initial='2000-01-01')

    primeira_contribuicao = forms.DateField(initial='2000-01-01')

    ultima_contribuicao = forms.DateField(initial='2019-01-01')
