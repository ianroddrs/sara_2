from apps.phoenix.forms import BOP_SearchForm, Procedure_SearchForm, Report_SearchForm, Person_SearchForm

def search_forms_context(request):
    """
    Adiciona os formulários de pesquisa da aplicação Phoenix ao contexto
    de todos os templates.
    """
    return {
        'bop_search_form': BOP_SearchForm(),
        'procedure_search_form': Procedure_SearchForm(),
        'report_search_form': Report_SearchForm(),
        'person_search_form': Person_SearchForm(),
    }