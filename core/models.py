from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta

# Modelo para as Aplicações/Módulos do sistema
class Application(models.Model):
    name = models.CharField(
        _("Nome da Aplicação"),
        max_length=100,
        unique=True,
        help_text=_("Ex: Phoenix, Análise de Dados")
    )
    # NOVO CAMPO: Liga a aplicação ao namespace da URL
    app_namespace = models.CharField(
        _("Namespace da Aplicação (para URLs)"),
        max_length=50,
        unique=True,
        help_text=_("O 'app_name' definido no urls.py da aplicação. Ex: 'phoenix'")
    )
    description = models.TextField(_("Descrição"), blank=True)

    class Meta:
        verbose_name = _("Aplicação")
        verbose_name_plural = _("Aplicações")
        ordering = ['name']

    def __str__(self):
        return self.name

class Module(models.Model):
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
        _("Nome da View (url name)"),
        max_length=100,
        # 'unique=True' foi removido daqui
        help_text=_("O 'name' da URL no urls.py. Ex: 'dashboard', 'user_list'")
    )
    description = models.TextField(_("Descrição"), blank=True)

    class Meta:
        verbose_name = _("Módulo")
        verbose_name_plural = _("Módulos")
        ordering = ['application', 'name']
        # NOVA RESTRIÇÃO: O nome da view deve ser único DENTRO da aplicação
        unique_together = ('application', 'view_name')

    def __str__(self):
        return f"{self.application.name} - {self.name}"


# Modelo de Usuário Customizado (sem alterações aqui)
class CustomUser(AbstractUser):
    # ... (código existente sem alterações)
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