from django.db import models


# Create your models here.
GENDER_CHOICES = (
    ('M', u'Masculino'),
    ('F', u'Feminino'),
)


class Aposentados(models.Model):

    nome = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField()
    tempo_contribuicao = models.IntegerField()
    valor_contribuicao = models.FloatField()
    valor_aposentadoria = models.FloatField()
