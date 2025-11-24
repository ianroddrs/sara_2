from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.base.decorators import secure_module_access

@secure_module_access
def home(request):
    """
    Exibe a página principal da aplicação Phoenix com o histórico 
    de pesquisas e itens salvos do usuário.
    """
    context = {}
    return render(request, 'phoenix.html', context)