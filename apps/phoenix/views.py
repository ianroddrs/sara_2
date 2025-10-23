from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.base.decorators import module_access_required

@login_required
@module_access_required
def home(request):
    """
    Exibe a página principal da aplicação Phoenix com o histórico 
    de pesquisas e itens salvos do usuário.
    """
    context = {
        'show_info_panel': True
    }
    return render(request, 'phoenix/phoenix.html', context)