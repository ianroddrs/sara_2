from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def module_access_required(view_func):
    """
    Decorator para views que verifica se o usuário tem permissão
    para acessar um módulo. Ele descobre automaticamente o nome da view
    sendo executada a partir do objeto request.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Superusuários têm acesso a tudo
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # Pega o nome da view resolvida dinamicamente (ex: 'phoenix:dashboard')
        # request.resolver_match é o objeto que contém os detalhes da URL resolvida
        view_name = request.resolver_match.view_name
        
        # Se não houver um nome de view (improvável em views nomeadas), nega o acesso
        if not view_name:
            messages.error(request, "Erro de configuração de permissão (view sem nome).")
            return redirect('core:user_list')

        # Verifica se o usuário tem o módulo específico em sua lista de permissões
        if request.user.modules.filter(view_name=view_name).exists():
            return view_func(request, *args, **kwargs)
        
        # Se não tiver permissão
        messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
        return redirect('core:user_list')
    
    return _wrapped_view