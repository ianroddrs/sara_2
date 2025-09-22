from django.contrib.auth.models import Group

def get_user_group_level(user):
    """
    Retorna o nível hierárquico de um usuário.
    Níveis mais baixos representam maior poder.
    """
    if user.is_superuser or user.groups.filter(name='Administrador').exists():
        return 1
    if user.groups.filter(name='Coordenador').exists():
        return 2
    if user.groups.filter(name='Gerente').exists():
        return 3
    if user.groups.filter(name='Usuário').exists():
        return 4
    return 5 # Sem grupo

def user_can_manage_other(requesting_user, target_user):
    """
    Verifica se o `requesting_user` tem permissão para gerenciar o `target_user`
    com base na hierarquia de grupos.
    """
    # Ninguém pode gerenciar a si mesmo, exceto para o próprio perfil
    if requesting_user == target_user:
        return False
        
    requesting_level = get_user_group_level(requesting_user)
    target_level = get_user_group_level(target_user)

    # Um usuário só pode gerenciar outro se seu nível for estritamente superior (menor número)
    return requesting_level < target_level
