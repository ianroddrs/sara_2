# Este arquivo deve ser criado manualmente após rodar `makemigrations` pela primeira vez.
# python manage.py makemigrations core
# Crie o arquivo 0002_create_groups.py e cole este conteúdo.

from django.db import migrations
from django.contrib.auth.models import Group

def create_user_groups(apps, schema_editor):
    """
    Cria os grupos de usuários padrão no sistema.
    Esta migração é executada uma vez para popular o banco de dados
    com os grupos hierárquicos necessários.
    """
    groups = ["Administrador", "Coordenador", "Gerente", "Usuário"]
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)

class Migration(migrations.Migration):

    dependencies = [
        # Depende da migração anterior do seu app (geralmente '0001_initial')
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_user_groups),
    ]
