from datetime import datetime
from math import floor

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import FormView, ListView, DeleteView, UpdateView
from website.forms import SimulacaoForm
from website.models import Simulacoes


class AposentadosList(ListView):
    model = Simulacoes
    template_name = 'listar.html'


class AposentadosDelete(DeleteView):
    model = Simulacoes

    def get_success_url(self):
        return reverse('listar')


@login_required
def updateAposentado(request, key):
    model = Simulacoes.objects.get(id=key)
    form = SimulacaoForm(instance=model)

    return render(request, 'index.html', {'form': form})


class Aposentar(FormView):
    template_name = 'index.html'
    form_class = SimulacaoForm

    def form_valid(self, form):
        data = form.save(commit=False)
        data.valor_aposentadoria = Simulacao.calcular_valor_aposentadoria(data)
        data.save()
        return reverse('listar')


class Simulacao(FormView):
    template_name = 'index.html'
    form_class = SimulacaoForm
    data_return = None

    def error_message(self, form, message):
        self.data_return = {'form': form, 'error_message': message}

    def confirm_save(self, form, message):
        self.data_return = {'form': form, 'confirm_message': message}

    def form_valid(self, form):
        # Removendo dados anteriores do cpf para não ter dados repetidos
        data = form.save(commit=False)
        Simulacoes.objects.filter(cpf=data.cpf).delete()
        data.save()

        pode_aposentar = self.verificar_requisitos(form)

        if pode_aposentar is True:
            self.calcular_aposentadoria(form)

        return render(self.request, 'index.html', self.data_return)

    ''' Verificar os requisitos para aposentar '''
    def verificar_requisitos(self, form):
        data = form.data
        idade = self.calcular_idade(data)
        esta_no_pedagio = False
        pode_aposentar = True

        ''' Idade minima para se aposentar Homem: 65 anos, Mulher: 62 anos'''
        idade_min_m = 65
        idade_min_f = 62

        ''' 
                Caso o cliente tenha cumprido os 35, mas não tenha idade, este poderá aposentar se tiver a idade: 
                Mulher: 53 anos, Homem: 55 anos;
        '''
        anos_contribuicao = 10# int(data['tempo_contribuicao'])
        if anos_contribuicao >= 35:
            idade_min_m = 55
            idade_min_f = 53

        idade_faltante = (idade_min_m if data['sexo'] == 'M' else idade_min_f) - idade
        contribuicao_faltante = 25 - anos_contribuicao

        ''' 
            Pedágio: caso falte apenas 5 anos para aposentar, aplicar-se-á o pedágio. 
            Será acrescido no tempo de contribuição 30%;
        '''
        if contribuicao_faltante <= 5:
            anos_contribuicao += (anos_contribuicao * 0.3)
            contribuicao_faltante = 25 - anos_contribuicao
            esta_no_pedagio = True

        if anos_contribuicao < 25 or idade_faltante > 0:
            pode_aposentar = False
            message = "Faltam {} anos para você aposentar!".format(idade_faltante)

            if esta_no_pedagio is True:
                message = "Você está na regra do pedágio! Espere só mais um pouco. " \
                          "Faltam apenas {} anos para você poder se aposentar"\
                    .format(max(contribuicao_faltante, idade_faltante))

            self.error_message(form, message)

        return pode_aposentar

    ''' Calcular valor da aposentadoria '''
    def calcular_aposentadoria(self, form):
        data = form.data
        valor_aposentadoria = self.calcular_valor_aposentadoria(data)

        message = "Parabéns, você pode aposentar! O valor da aposentadoria será R$ {}. Deseja aposentar hoje?"\
            .format(self.real_br_money_mask(valor_aposentadoria))
        self.confirm_save(form, message)

    @staticmethod
    def calcular_valor_aposentadoria(data):
        valor_total_contribuido = 0
        anos_contribuicao = 3# int(data['tempo_contribuicao'])
        valor_contribuicao = 5#float(data['valor_contribuicao'])

        for i in range(anos_contribuicao):
            valor_total_contribuido += valor_contribuicao * i

        media = valor_total_contribuido / anos_contribuicao
        valor_inicial = media * 0.7
        valor_aposentadoria = valor_inicial

        if 25 < anos_contribuicao <= 30:
            valor_aposentadoria = valor_inicial + media * (0.015 * (anos_contribuicao - 25))

        if 30 < anos_contribuicao <= 35:
            valor_aposentadoria = valor_inicial + media * (0.02 * (anos_contribuicao - 30))

        if anos_contribuicao > 35:
            valor_aposentadoria = valor_inicial + anos_contribuicao * (0.025 * (anos_contribuicao - 35))

        return valor_aposentadoria

    def calcular_idade(self, data):
        data_nascimento = datetime.strptime(data['nascimento'], '%Y-%m-%d').date()
        actual_date = datetime.strptime(data['ultima_contribuicao'], '%Y-%m-%d').date()
        idade = floor((actual_date - data_nascimento).days / 365)
        return idade

    def real_br_money_mask(self, my_value):
        a = '{:,.2f}'.format(float(my_value))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        return c.replace('v', '.')
