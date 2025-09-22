from django import template
from core.utils import user_can_manage_other, get_user_group_level

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Verifica se um usuário pertence a um grupo específico.
    Uso: {% if request.user|has_group:"Gerente" %}
    """
    return user.groups.filter(name=group_name).exists()

@register.filter(name='is_manageable_by')
def is_manageable_by(target_user, requesting_user):
    """
    Verifica se o target_user pode ser gerenciado pelo requesting_user.
    Uso: {% if some_user|is_manageable_by:request.user %}
    """
    return user_can_manage_other(requesting_user, target_user)

@register.simple_tag
def get_group(user):
    """
    Retorna o nome do primeiro grupo do usuário.
    Uso: {% get_group user %}
    """
    return user.groups.first().name if user.groups.exists() else 'Sem Grupo'
