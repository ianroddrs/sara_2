from django.urls import path
from . import views

app_name = 'phoenix'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Adicionaremos as URLs dos resultados da pesquisa aqui no futuro
]