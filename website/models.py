from django.db import models


# Create your models here.
GENDER_CHOICES = (
    ('M', u'Masculino'),
    ('F', u'Feminino'),
)


class Simulacoes(models.Model):

    nome = models.CharField(max_length=255)
    sexo = models.CharField(max_length=1, choices=GENDER_CHOICES)
    cpf = models.CharField(max_length=14)
    nascimento = models.DateField()
    primeira_contribuicao = models.DateField()
    ultima_contribuicao = models.DateField()
    ano1 = models.FloatField()
    ano2 = models.FloatField()
    ano3 = models.FloatField()
    ano4 = models.FloatField()
    ano5 = models.FloatField()
    ano6 = models.FloatField()
    ano7 = models.FloatField()
    ano8 = models.FloatField()
    ano9 = models.FloatField()
    ano10 = models.FloatField()
    valor_aposentadoria = models.FloatField(null=True, blank=True)
