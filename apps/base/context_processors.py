from apps.phoenix.forms import BOP_SearchForm, Procedure_SearchForm, Report_SearchForm, Person_SearchForm
from apps.base.forms import CustomPasswordChangeForm, CustomUserChangeForm

def forms_context(request):
    """
    Adiciona os formulários ao contexto.
    Verifica se o usuário está logado antes de instanciar forms de usuário.
    """
    context = {
        # Formulários de pesquisa (não dependem de usuário logado)
        'bop_search_form': BOP_SearchForm(),
        'procedure_search_form': Procedure_SearchForm(),
        'report_search_form': Report_SearchForm(),
        'person_search_form': Person_SearchForm(),
    }

    # Só tentamos criar os forms de senha/perfil se o usuário estiver autenticado
    if request.user.is_authenticated:
        context['password_change_form'] = CustomPasswordChangeForm(user=request.user)
        context['user_change_form'] = CustomUserChangeForm(instance=request.user)
    return context