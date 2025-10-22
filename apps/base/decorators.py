from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def module_access_required(view_func):
    """
    Decorator para views que verifica se o usuário tem permissão para acessar um
    módulo, usando tanto o namespace da aplicação quanto o nome da view para
    uma verificação precisa.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        resolver_match = request.resolver_match
        
        # Pega o namespace da app (ex: 'phoenix') e o nome da url (ex: 'dashboard')
        app_namespace = resolver_match.app_name
        url_name = resolver_match.url_name

        if not app_namespace or not url_name:
            messages.error(request, "Erro de configuração de permissão (URL sem namespace ou nome).")
            return redirect('core:user_list')

        # A verificação agora é composta, garantindo a unicidade da permissão
        if request.user.modules.filter(
            application__app_namespace=app_namespace,
            view_name=url_name
        ).exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
        return redirect('core:user_list')
    
    return _wrapped_view