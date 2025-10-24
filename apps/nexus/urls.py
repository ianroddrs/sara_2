from django.urls import path
from . import views

app_name = 'nexus'

urlpatterns = [
    path('', views.home, name='nexus'),
    # Adicionaremos as URLs dos resultados da pesquisa aqui no futuro
]