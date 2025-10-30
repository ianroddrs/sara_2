from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.base.decorators import module_access_required, login_required_with_message

# @login_required
@login_required_with_message
@module_access_required
def home(request):
    """
    Exibe a página principal da aplicação Phoenix com o histórico 
    de pesquisas e itens salvos do usuário.
    """
    context = {
        'info_panel': True
    }
    return render(request, 'phoenix.html', context)