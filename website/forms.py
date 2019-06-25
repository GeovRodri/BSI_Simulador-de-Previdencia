from django.forms import ModelForm
from website.models import Simulacoes


class SimulacaoForm(ModelForm):
    class Meta:
        model = Simulacoes
        fields = '__all__'


class AposentadoriaForm(ModelForm):
    class Meta:
        model = Simulacoes
        fields = '__all__'
