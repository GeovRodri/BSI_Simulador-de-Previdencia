from datetime import datetime
from math import floor

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.generic import FormView
from website.forms import SimulacaoForm


class Simulacao(FormView):
    template_name = 'index.html'
    form_class = SimulacaoForm

    def form_valid(self, form):
        data = form.data
        idade_min_m = 65
        idade_min_f = 62

        data_nascimento = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        tempo_contribuicao = datetime.strptime(data['data_nascimento'], '%Y-%m-%d').date()
        actual_date = datetime.now().date()

        idade = floor((actual_date - data_nascimento).days / 365)
        anos_contribuicao = floor((actual_date - tempo_contribuicao).days / 365)

        if anos_contribuicao >= 35:
            idade_min_m = 55
            idade_min_f = 53

        try:
            if anos_contribuicao < 25:
                raise ValidationError('')

            if (data['sexo'] == 'M' and idade < idade_min_m) or (data['sexo'] == 'F' and idade < idade_min_f):
                raise ValidationError('')

            form.data['tempo_contribuicao'] = 4
        except ValidationError:
            message = "Faltam {} anos para você aposentar!"\
                .format((idade_min_m if data['sexo'] == 'M' else idade_min_f) - idade)
            return render(self.request, 'index.html', {'form': form, 'error_message': message})
