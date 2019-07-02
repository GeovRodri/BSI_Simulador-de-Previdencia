from datetime import datetime


class Utils:

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
        return Utils.calcular_inflacao(valor, (ano + 1))