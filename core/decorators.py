from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def module_access_required(view_name):
    """
    Decorator para views que verifica se o usuário tem permissão
    para acessar um módulo específico (identificado pelo seu view_name).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Superusuários têm acesso a tudo
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Verifica se o usuário tem o módulo específico em sua lista de permissões
            if request.user.modules.filter(view_name=view_name).exists():
                return view_func(request, *args, **kwargs)
            
            # Se não tiver permissão
            messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
            # Redireciona para a home page ou outra página de 'acesso negado'
            return redirect('core:user_list')
        return _wrapped_view
    return decorator