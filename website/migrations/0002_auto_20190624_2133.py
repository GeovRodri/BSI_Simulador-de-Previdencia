# Generated by Django 2.2.1 on 2019-06-25 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Simulacoes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255)),
                ('sexo', models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], max_length=1)),
                ('cpf', models.CharField(max_length=14)),
                ('nascimento', models.DateField()),
                ('primeira_contribuicao', models.DateField()),
                ('ultima_contribuicao', models.DateField()),
                ('ano1', models.FloatField()),
                ('ano2', models.FloatField()),
                ('ano3', models.FloatField()),
                ('ano4', models.FloatField()),
                ('ano5', models.FloatField()),
                ('ano6', models.FloatField()),
                ('ano7', models.FloatField()),
                ('ano8', models.FloatField()),
                ('ano9', models.FloatField()),
                ('ano10', models.FloatField()),
                ('valor_aposentadoria', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Aposentados',
        ),
    ]
