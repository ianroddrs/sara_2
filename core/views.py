from django.contrib.auth.views import LoginView as BaseLoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from collections import defaultdict
from .models import Application
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    AdminUserUpdateForm,
    CustomPasswordChangeForm,
    AdminPasswordChangeForm
)
from .utils import user_can_manage_other # Lógica de hierarquia

CustomUser = get_user_model()

# --- Lógica de Autenticação com Validação de IP ---
class CustomLoginView(BaseLoginView):
    template_name = 'core/login.html'

    def form_valid(self, form):
        user = form.get_user()
        
        # Validação Crítica de IP
        if user.allowed_ip_address:
            # Obtém o IP real, considerando proxies
            x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                request_ip = x_forwarded_for.split(',')[0]
            else:
                request_ip = self.request.META.get('REMOTE_ADDR')

            if user.allowed_ip_address != request_ip:
                messages.error(self.request, "Acesso negado. Você está tentando acessar de um endereço de IP não autorizado.")
                return self.form_invalid(form)
        
        # Se o IP for válido ou não houver restrição, prossegue com o login
        login(self.request, user)
        return redirect(self.get_success_url())

# --- Mixins de Permissão Hierárquica ---
class ManagerialRoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que garante que o usuário pertence a um grupo gerencial
    (Administrador, Coordenador ou Gerente).
    """
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administrador', 'Coordenador', 'Gerente']).exists()

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para acessar esta página.")
        return redirect('core:user_list')

# --- Views de Gerenciamento de Usuários ---

class UserManagementView(ManagerialRoleRequiredMixin, ListView):
    """
    Painel de Gerenciamento de Usuários.
    Exibe usuários que o usuário logado pode gerenciar.
    """
    model = CustomUser
    template_name = 'core/user_management.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        # Administradores veem todos
        if user.groups.filter(name='Administrador').exists():
            return CustomUser.objects.all().prefetch_related('groups')
        
        # Coordenadores veem Gerentes e Usuários, além de outros Coordenadores
        if user.groups.filter(name='Coordenador').exists():
            return CustomUser.objects.filter(
                groups__name__in=['Coordenador', 'Gerente', 'Usuário']
            ).distinct().prefetch_related('groups')

        # Gerentes veem Usuários, além de outros Gerentes
        if user.groups.filter(name='Gerente').exists():
            return CustomUser.objects.filter(
                groups__name__in=['Gerente', 'Usuário']
            ).distinct().prefetch_related('groups')
            
        return CustomUser.objects.none() # Se não for nenhum dos acima

class UserCreateView(ManagerialRoleRequiredMixin, CreateView):
    """
    View para criar novos usuários, respeitando a hierarquia.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'core/profile_form.html'
    success_url = reverse_lazy('core:user_management')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['requesting_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f"Usuário {form.cleaned_data.get('username')} criado com sucesso!")
        return super().form_valid(form)

class UserUpdateView(ManagerialRoleRequiredMixin, UpdateView):
    """
    View para editar um usuário existente.
    A permissão para editar é verificada pelo `user_can_manage_other`.
    """
    model = CustomUser
    form_class = AdminUserUpdateForm
    template_name = 'core/profile_form.html'
    success_url = reverse_lazy('core:user_management')
    
    def get_object(self, queryset=None):
        # Garante que o usuário só possa editar quem ele tem permissão
        obj = super().get_object(queryset)
        if not user_can_manage_other(self.request.user, obj):
            raise PermissionDenied("Você не tem permissão para editar este usuário.")
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['requesting_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Usuário atualizado com sucesso!")
        return super().form_valid(form)

class UserDeleteView(ManagerialRoleRequiredMixin, DeleteView):
    """
    View para excluir um usuário, com verificação de hierarquia.
    """
    model = CustomUser
    template_name = 'core/user_confirm_delete.html'
    success_url = reverse_lazy('core:user_management')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not user_can_manage_other(self.request.user, obj):
            raise PermissionDenied("Você não tem permissão para excluir este usuário.")
        return obj

    def post(self, request, *args, **kwargs):
        username = self.get_object().username
        messages.success(request, f"Usuário {username} excluído com sucesso!")
        return super().post(request, *args, **kwargs)


# --- Views Públicas e de Perfil ---

class UserListView(LoginRequiredMixin, ListView):
    """
    Lista pública de todos os usuários do sistema.
    """
    model = CustomUser
    template_name = 'core/user_list.html'
    context_object_name = 'users'
    queryset = CustomUser.objects.all().prefetch_related('groups')

class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Exibe o perfil de um usuário, incluindo uma lista completa
    de permissões de módulos (concedidas e negadas).
    """
    model = CustomUser
    template_name = 'core/user_profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()

        # Busca todas as aplicações com seus respectivos módulos para a lista completa
        all_applications = Application.objects.prefetch_related('modules').order_by('name')

        # Busca os IDs dos módulos que o usuário realmente possui
        user_module_ids = set(profile_user.modules.values_list('id', flat=True))

        # Adiciona ambas as informações ao contexto
        context['all_applications'] = all_applications
        context['user_module_ids'] = user_module_ids
        
        return context

@login_required
def self_profile_update_view(request):
    """
    Permite que o usuário edite suas próprias informações básicas.
    """
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('core:user_profile', pk=request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'core/profile_form.html', {'form': form})

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    Permite que o usuário altere sua própria senha.
    """
    form_class = CustomPasswordChangeForm
    template_name = 'core/password_change_form.html'
    success_url = reverse_lazy('core:user_list') # Redirecionar para um lugar apropriado

    def form_valid(self, form):
        messages.success(self.request, "Sua senha foi alterada com sucesso!")
        return super().form_valid(form)

# --- Views de Gerenciamento de Acesso às Aplicações ---
@login_required
def manage_user_access_view(request, pk):
    """
    Gerencia quais MÓDULOS um usuário específico pode acessar,
    agrupados por Aplicação.
    """
    target_user = get_object_or_404(CustomUser, pk=pk)

    if not user_can_manage_other(request.user, target_user):
        messages.error(request, "Você não tem permissão para gerenciar os acessos deste usuário.")
        return redirect('core:user_management')
    
    if request.method == 'POST':
        # Pega a lista de IDs dos módulos selecionados no formulário
        module_ids = request.POST.getlist('modules')
        # O método set() convenientemente limpa as permissões antigas e adiciona as novas
        target_user.modules.set(module_ids)
        
        messages.success(request, f"Acessos do usuário {target_user.username} atualizados.")
        return redirect('core:user_management')

    # Para o método GET
    # Busca todas as aplicações com seus respectivos módulos para montar a tela
    applications = Application.objects.prefetch_related('modules').all()
    # Busca os IDs dos módulos que o usuário já possui
    user_module_ids = set(target_user.modules.values_list('id', flat=True))

    context = {
        'target_user': target_user,
        'applications': applications,
        'user_module_ids': user_module_ids
    }
    return render(request, 'core/manage_user_access.html', context)

@login_required
def user_password_change_view(request, pk):
    """
    Permite que um usuário com hierarquia superior altere a senha de um usuário inferior.
    """
    target_user = get_object_or_404(CustomUser, pk=pk)

    if not user_can_manage_other(request.user, target_user):
        messages.error(request, "Você não tem permissão para alterar a senha deste usuário.")
        return redirect('core:user_management')

    if request.method == 'POST':
        form = AdminPasswordChangeForm(target_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"A senha de {target_user.username} foi alterada com sucesso.")
            return redirect('core:user_management')
    else:
        form = AdminPasswordChangeForm(target_user)

    return render(request, 'core/admin_password_change_form.html', {
        'form': form,
        'target_user': target_user
    })