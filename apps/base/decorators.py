from functools import wraps
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe

def secure_module_access(view_func):
    """
    Decorador unificado que gerencia autenticação e permissão.
    Previne loops de redirecionamento verificando o HTTP_REFERER.
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
            
            # Adiciona a mensagem apenas se ela já não estiver lá (evita spam de mensagens no loop/refresh)
            # Opcional, mas recomendado
            storage = messages.get_messages(request)
            if not any(msg.message == message_text for msg in storage):
                 messages.error(request, mark_safe(message_text))
            
            # --- Lógica de Correção do Loop ---
            referer = request.META.get('HTTP_REFERER')
            home_url = reverse('base:home') # Certifique-se que 'base:home' existe, ou use apenas 'home'
            
            if referer:
                # Extrai apenas o caminho (path) do referer para comparar, ignorando domínio e query string
                try:
                    referer_path = urlparse(referer).path
                except ValueError:
                    referer_path = None
                
                # SE o lugar de onde vim (referer) É o mesmo lugar onde estou (request.path)
                # ENTÃO jogue para a home, senão teremos loop infinito.
                if referer_path == request.path:
                    target_url = home_url
                else:
                    target_url = referer
            else:
                target_url = home_url
            
            # ----------------------------------

            current_url = request.get_full_path()
            
            # Montagem da URL com o parametro 'next'
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
        # 4. Acesso Negado (Logado, mas sem permissão)
        # ---------------------------------------------------------
        messages.error(request, "Você não tem permissão para acessar esta funcionalidade.")
        return redirect('base:home')
    
    return _wrapped_view