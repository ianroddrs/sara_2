from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

# Modelo para as Aplicações/Módulos do sistema
class Application(models.Model):
    """
    Representa um módulo ou aplicação dentro da plataforma.
    É o container de alto nível para agrupar funcionalidades.
    """
    name = models.CharField(
        _("Nome da Aplicação"),
        max_length=100,
        unique=True,
        help_text=_("Ex: Phoenix, Nexus")
    )
    description = models.TextField(_("Descrição"), blank=True)

    class Meta:
        verbose_name = _("Aplicação")
        verbose_name_plural = _("Aplicações")
        ordering = ['name']

    def __str__(self):
        return self.name

class Module(models.Model):
    """
    Representa uma view ou funcionalidade específica dentro de uma Application,
    sendo a unidade final para o controle de acesso.
    """
    application = models.ForeignKey(
        Application,
        related_name='modules',
        on_delete=models.CASCADE,
        verbose_name=_("Aplicação")
    )
    name = models.CharField(
        _("Nome do Módulo"),
        max_length=100,
        help_text=_("Ex: Dashboard de Ocorrências, Pesquisa por BOP")
    )
    view_name = models.CharField(
        _("Nome da View (para verificação)"),
        max_length=100,
        unique=True,
        help_text=_("Identificador único da URL/View. Ex: 'phoenix:dashboard'")
    )
    description = models.TextField(_("Descrição"), blank=True)

    class Meta:
        verbose_name = _("Módulo")
        verbose_name_plural = _("Módulos")
        ordering = ['application', 'name']

    def __str__(self):
        return f"{self.application.name} - {self.name}"


# Modelo de Usuário Customizado
class CustomUser(AbstractUser):
    """
    Herda do usuário padrão do Django, com controle de acesso
    baseado em Módulos.
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
    last_activity = models.DateTimeField(
        _("Última Atividade"),
        null=True,
        blank=True
    )
    # Relação direta com os Módulos que o usuário pode acessar
    modules = models.ManyToManyField(
        Module,
        related_name='users',
        blank=True,
        verbose_name=_("Módulos com Acesso")
    )

    class Meta:
        verbose_name = _("Usuário")
        verbose_name_plural = _("Usuários")
        ordering = ['username']

    def is_online(self):
        """Verifica se a última atividade do usuário foi nos últimos 5 minutos."""
        if not self.last_activity:
            return False
        return timezone.now() < self.last_activity + timedelta(minutes=5)
