from django.shortcuts import render
from django.views.generic import FormView
from website.forms import SimulacaoForm


class Simulacao(FormView):
    template_name = 'index.html'
    form_class = SimulacaoForm
