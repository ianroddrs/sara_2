from django import forms
from .models import Localidades, Consolidados

class BOP_SearchForm(forms.Form):
    nro_bop = forms.CharField(label="Número do Boletim", max_length=100)

class Procedure_SearchForm(forms.Form):
    nro_tombo = forms.CharField(label="Número do Procedimento", max_length=100)

class Report_SearchForm(forms.Form):
    relato = forms.CharField(label="Termos do Relato", widget=forms.Textarea(attrs={'rows': 3}))
    data_inicio = forms.DateField(label="Data de Início (Opcional)", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label="Data de Fim (Opcional)", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    municipio = forms.ModelChoiceField(queryset=Localidades.objects.values_list('municipios', flat=True).distinct(), label="Município (Opcional)", required=False)
    consolidado = forms.ModelChoiceField(queryset=Consolidados.objects.values_list('consolidado', flat=True).distinct(), label="Tipo de Crime (Opcional)", required=False)

class Person_SearchForm(forms.Form):
    nome = forms.CharField(label="Nome do Autor ou Vítima", max_length=200)
    data_inicio = forms.DateField(label="Data de Início (Opcional)", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    data_fim = forms.DateField(label="Data de Fim (Opcional)", required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    municipio = forms.ModelChoiceField(queryset=Localidades.objects.values_list('municipios', flat=True).distinct(), label="Município (Opcional)", required=False)
    consolidado = forms.ModelChoiceField(queryset=Consolidados.objects.values_list('consolidado', flat=True).distinct(), label="Tipo de Crime (Opcional)", required=False)