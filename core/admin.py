from django.contrib import admin
from .models import Application, Module, CustomUser

class ModuleInline(admin.TabularInline):
    """Permite editar módulos diretamente na tela da aplicação."""
    model = Module
    extra = 1 # Quantos formulários em branco exibir
    ordering = ('name',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    inlines = [ModuleInline]

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'application', 'view_name')
    list_filter = ('application',)
    search_fields = ('name', 'view_name')
