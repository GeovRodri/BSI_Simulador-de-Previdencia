from datetime import datetime, timedelta
from math import floor
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import FormView, ListView, DeleteView
from website.forms import SimulacaoForm
from website.models import Simulacoes


class AposentadosList(ListView):
    model = Simulacoes
    template_name = 'listar.html'


class AposentadosDelete(DeleteView):
    model = Simulacoes

    def get_success_url(self):
        return redirect('listar')


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
        Simulacoes.objects.filter(cpf=data.cpf).delete()

        (valor_aposentadoria, media, tempo) = Simulacao.calcular_valor_aposentadoria(data)
        data.valor_aposentadoria = min(valor_aposentadoria, 5531.31)
        data.aposentado = True
        data.apto = True
        data.save()
        return redirect('listar')


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

        pode_aposentar = False
        idade = self.calcular_idade(data)
        actual_date = datetime.now()
        sexo = data.sexo

        ''' 
            Caso o cliente tenha cumprido os 35, mas não tenha idade, este poderá aposentar se tiver a idade: 
            Mulher: 53 anos, Homem: 55 anos;
        '''
        anos_contribuicao = Simulacao.calcular_ano_de_contribuicao(data)
        contribuicao_faltante = (35 if data.sexo == 'M' else 30) - anos_contribuicao
        data_aposentadoria = actual_date + timedelta(days=(contribuicao_faltante * 365))
        (valor_aposentadoria, media_salarial, tempo) = self.calcular_valor_aposentadoria(data)

        if anos_contribuicao >= 35 and ((sexo == 'M' and idade > 55) or (sexo == 'F' and idade > 53)):
            pode_aposentar = True

        if anos_contribuicao >= 25 and ((sexo == 'M' and idade > 65) or (sexo == 'F' and idade > 62)):
            pode_aposentar = True

        ''' 
            Pedágio: Se faltam 9 anos para um homem completar 35 anos de contribuição ou para a mulher completar 30,
            será preciso trabalhar um pouco mais. No caso deste exemplo quase 3 anos.
        '''
        if contribuicao_faltante <= 9:
            nova_idade_faltante = contribuicao_faltante + (contribuicao_faltante * 0.3)
            data_aposentadoria = actual_date + timedelta(days=(nova_idade_faltante * 365))

            message = u"Você está na regra do pedágio! Espere só mais um pouco. " \
                      u"Faltam apenas {} anos para você poder se aposentar. " \
                      u"Na antiga previdencia você iria se aposentar daqui {}. " \
                      u"Sua idade é {}, o seu tempo de contribuição é {} anos e a data da sua aposentadoria será {}. " \
                      u"E o valor atual da sua aposentadoria é {}" \
                .format(nova_idade_faltante, contribuicao_faltante, idade, anos_contribuicao,
                        data_aposentadoria.strftime('%d/%m/%Y'), self.real_br_money_mask(valor_aposentadoria))

            self.error_message(form, message)

        if pode_aposentar is False:
            message = u"Faltam {} anos para você aposentar! Sua idade é {} anos, o seu tempo de contribuição " \
                      u"é de {} anos, a data da sua aposentadoria será {} e o valor dela é {}" \
                .format(contribuicao_faltante, idade, anos_contribuicao, data_aposentadoria.strftime('%d/%m/%Y'),
                        self.real_br_money_mask(valor_aposentadoria))

            self.error_message(form, message)
        else:
            data.valor_aposentadoria = valor_aposentadoria
            message = u"Parabéns, você pode aposentar! O valor da aposentadoria será R$ {}." \
                .format(self.real_br_money_mask(min(valor_aposentadoria, 5531.31)))

            if valor_aposentadoria >= 5531.31:
                message += u"Você atingiu o teto salarial com o valor {}"\
                    .format(self.real_br_money_mask(valor_aposentadoria))

            message += u" Deseja aposentar hoje? Sua media salarial é {}, idade é {} anos e o tempo de contribuição {}"\
                .format(media_salarial, idade, tempo)
            self.confirm_save(form, message)

        data.apto = pode_aposentar
        data.save()
        return render(self.request, 'index.html', self.data_return)

    @staticmethod
    def calcular_ano_de_contribuicao(data):
        primeira_contribuicao = data.primeira_contribuicao
        ultima_contribuicao = data.ultima_contribuicao
        anos_contribuicao = floor(abs(ultima_contribuicao - primeira_contribuicao).days / 365)
        return anos_contribuicao

    @staticmethod
    def calcular_valor_aposentadoria(data):
        anos_contribuicao = Simulacao.calcular_ano_de_contribuicao(data)
        ano_simulacao = data.ultima_contribuicao.year

        """ Calcular todo valor contribuido e a média de valor """
        valor_contribuicao = 0
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano1, (ano_simulacao - 9))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano2, (ano_simulacao - 8))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano3, (ano_simulacao - 7))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano4, (ano_simulacao - 6))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano5, (ano_simulacao - 5))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano6, (ano_simulacao - 4))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano7, (ano_simulacao - 3))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano8, (ano_simulacao - 2))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano9, (ano_simulacao - 1))
        valor_contribuicao += Simulacao.calcular_inflacao(data.ano10, ano_simulacao)
        media = valor_contribuicao / 10

        valor_inicial = media * 0.7
        valor_aposentadoria = valor_inicial

        if 25 < anos_contribuicao <= 30:
            valor_aposentadoria = valor_inicial + media * (0.015 * (anos_contribuicao - 25))

        if 30 < anos_contribuicao <= 35:
            valor_aposentadoria = valor_inicial + media * (0.02 * (anos_contribuicao - 30))

        if anos_contribuicao > 35:
            valor_aposentadoria = valor_inicial + anos_contribuicao * (0.025 * (anos_contribuicao - 35))

        return valor_aposentadoria, media, anos_contribuicao

    @staticmethod
    def calcular_inflacao(valor, ano):
        valor = float(valor)
        ano_atual = datetime.now().year
        inflacoes = {'1997': 5.22, '1998': 1.65, '1999': 8.94, '2000': 5.97, '2001': 7.67, '2002': 12.53, '2003': 9.30,
                     '2004': 7.6, '2005': 5.69, '2006': 3.14, '2007': 4.46, '2008': 5.9, '2009': 4.31, '2010': 5.91,
                     '2011': 6.5, '2012': 5.84, '2013': 5.91, '2014': 6.41, '2015': 10.67, '2016': 6.29, '2017': 2.95,
                     '2018': 3.75}

        if ano == ano_atual:
            return valor

        valor += (inflacoes.get('{}'.format(ano), 2) * 100) / 100
        return Simulacao.calcular_inflacao(valor, (ano + 1))

    def calcular_idade(self, data):
        data_nascimento = data.nascimento
        actual_date = datetime.now().date()
        idade = floor((actual_date - data_nascimento).days / 365)
        return idade

    def real_br_money_mask(self, my_value):
        a = '{:,.2f}'.format(float(my_value))
        b = a.replace(',', 'v')
        c = b.replace('.', ',')
        return c.replace('v', '.')
