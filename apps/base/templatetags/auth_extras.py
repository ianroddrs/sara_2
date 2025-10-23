from django import template
from django.utils import timezone
from django.utils.timesince import timesince
from apps.base.utils import user_can_manage_other, get_user_group_level

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

@register.filter(name='humanize_last_activity')
def humanize_last_activity(last_activity_datetime):
    """
    Converte a data da última atividade em uma string legível.
    Ex: "há 5 minutos", "ontem", etc.
    """
    if not last_activity_datetime:
        return "Nunca"
    
    now = timezone.now()
    diff = now - last_activity_datetime

    if diff.days == 0 and diff.seconds < 60:
        return f"há {diff.seconds} segundos"
    if diff.days == 0 and diff.seconds < 3600:
        minutes = diff.seconds // 60
        return f"há {minutes} minuto{'s' if minutes > 1 else ''}"
    if diff.days == 0:
        hours = diff.seconds // 3600
        return f"há {hours} hora{'s' if hours > 1 else ''}"
    if 1 <= diff.days < 2:
        return "Ontem"
    
    return f"há {diff.days} dias"