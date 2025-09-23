from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import module_access_required

@login_required
@module_access_required('phoenix:dashboard')
def dashboard(request):
    """
    Exibe a página principal da aplicação Phoenix com o histórico 
    de pesquisas e itens salvos do usuário.
    """
    # Lógica para buscar histórico e itens salvos será adicionada aqui
    context = {
        'show_info_panel': True  # Adicione esta linha
    }
    return render(request, 'phoenix/dashboard.html', context)