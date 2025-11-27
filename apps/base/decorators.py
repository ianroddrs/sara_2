from functools import wraps
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.urls import reverse

def secure_module_access(view_func):
    """
    Decorador unificado que gerencia autenticação e permissão.
    Substitui o parâmetro 'next' se ele já existir na URL de destino.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        resolver_match = request.resolver_match
        
        # ---------------------------------------------------------
        # 1. Verificação de Autenticação
        # ---------------------------------------------------------
        if not request.user.is_authenticated:
            app_namespace = resolver_match.app_name if resolver_match and resolver_match.app_name else 'Aplicação'
            
            login_link = '<a href="#login-modal" data-bs-toggle="modal" data-bs-target="#login-modal"><strong class="text-primary text-decoration-none">autenticação</strong></a>'
            message_text = f"<strong>Acesso restrito</strong>. Faça {login_link} para acessar a aplicação <strong>{app_namespace.upper()}</strong>."
            messages.error(request, mark_safe(message_text))
            
            current_url = request.get_full_path()
            target_url = request.META.get('HTTP_REFERER') or reverse('home')
            

            parsed = urlparse(target_url)
            query_params = parse_qs(parsed.query)
            
            query_params['next'] = [current_url]
            new_query = urlencode(query_params, doseq=True)
            
            final_url = urlunparse((
                parsed.scheme,
                parsed.netloc,
                parsed.path,
                parsed.params,
                new_query,
                parsed.fragment
            ))

            return redirect(final_url)

        # ---------------------------------------------------------
        # 2. Verificação de Superusuário
        # ---------------------------------------------------------
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        # ---------------------------------------------------------
        # 3. Verificação de Permissão de Módulo
        # ---------------------------------------------------------
        app_namespace = resolver_match.app_name
        url_name = resolver_match.url_name

        if not app_namespace or not url_name:
            messages.error(request, "Erro de configuração de permissão (URL sem namespace ou nome).")
            return redirect('base:home')

        if request.user.modules.filter(
            application__app_namespace=app_namespace,
            view_name=url_name
        ).exists():
            return view_func(request, *args, **kwargs)
        
        # ---------------------------------------------------------
        # 4. Acesso Negado
        # ---------------------------------------------------------
        messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
        return redirect('base:home')
    
    return _wrapped_view