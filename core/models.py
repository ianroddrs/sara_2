from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Modelo para as Aplicações/Módulos do sistema
class Application(models.Model):
    """
    Representa um módulo ou aplicação dentro da plataforma, 
    cujo acesso pode ser controlado.
    """
    name = models.CharField(
        _("Nome da Aplicação"),
        max_length=100,
        unique=True,
        help_text=_("Ex: Dashboards de KPIs, Consulta ao Banco de Dados")
    )
    description = models.TextField(_("Descrição"), blank=True)

    class Meta:
        verbose_name = _("Aplicação")
        verbose_name_plural = _("Aplicações")
        ordering = ['name']

    def __str__(self):
        return self.name

# Modelo de Usuário Customizado
class CustomUser(AbstractUser):
    """
    Herda do usuário padrão do Django, adicionando campos específicos
    para foto de perfil e restrição de IP.
    """
    profile_picture = models.ImageField(
        _("Foto de Perfil"),
        upload_to='profile_pics/',
        default='profile_pics/default.jpg'
    )
    allowed_ip_address = models.CharField(
        _("IP de Acesso Permitido"),
        max_length=15,
        blank=True,
        null=True,
        help_text=_("Se vazio, o acesso é permitido de qualquer IP.")
    )
    # Relação Many-to-Many com as aplicações
    applications = models.ManyToManyField(
        Application,
        through='UserApplicationAccess',
        related_name='users',
        verbose_name=_("Aplicações")
    )

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        ordering = ['username']

# Modelo Intermediário para controle de acesso
class UserApplicationAccess(models.Model):
    """
    Tabela intermediária que conecta Usuários e Aplicações,
    controlando explicitamente se o acesso é permitido.
    """
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE,
        verbose_name=_("Usuário")
    )
    application = models.ForeignKey(
        Application, 
        on_delete=models.CASCADE,
        verbose_name=_("Aplicação")
    )
    has_access = models.BooleanField(
        _("Possui Acesso"),
        default=False
    )

    class Meta:
        verbose_name = _("Acesso de Usuário à Aplicação")
        verbose_name_plural = _("Acessos de Usuários às Aplicações")
        # Garante que cada usuário só tenha um registro de acesso por aplicação
        unique_together = ('user', 'application')

    def __str__(self):
        status = _("Permitido") if self.has_access else _("Negado")
        return f"{self.user.username} - {self.application.name}: {status}"
