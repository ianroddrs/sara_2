from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    Exibe a página principal da aplicação Phoenix com o histórico 
    de pesquisas e itens salvos do usuário.
    """
    # Lógica para buscar histórico e itens salvos será adicionada aqui
    context = {}
    return render(request, 'phoenix/dashboard.html', context)