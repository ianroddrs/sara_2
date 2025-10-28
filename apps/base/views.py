from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth import login, get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from .models import Application
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    AdminUserUpdateForm,
    CustomPasswordChangeForm,
    AdminPasswordChangeForm
)
from .utils import user_can_manage_other, get_online_user_ids

CustomUser = get_user_model()

def home(request):
    return render(request, "home.html")

# --- Lógica de Autenticação com Validação de IP ---
class CustomLoginView(BaseLoginView):
    template_name = 'base/login.html'

    def form_valid(self, form):
        user = form.get_user()
        
        if user.allowed_ip_address:
            x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                request_ip = x_forwarded_for.split(',')[0]
            else:
                request_ip = self.request.META.get('REMOTE_ADDR')

            if user.allowed_ip_address != request_ip:
                messages.error(self.request, "Acesso negado. Você está tentando acessar de um endereço de IP não autorizado.")
                return self.form_invalid(form)
        
        login(self.request, user)
        return redirect(self.get_success_url())

# --- Mixins de Permissão Hierárquica ---
class ManagerialRoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administrador', 'Coordenador', 'Gerente']).exists()

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para acessar esta página.")
        return redirect('core:user_list')

# --- Views de Gerenciamento de Usuários ---

class UserManagementView(ManagerialRoleRequiredMixin, ListView):
    model = CustomUser
    template_name = 'user_management.html'
    context_object_name = 'users'

    def get_queryset(self):
        # user = self.request.user
        # if user.groups.filter(name='Administrador').exists():
        return CustomUser.objects.all().prefetch_related('groups')
        # if user.groups.filter(name='Coordenador').exists():
        #     return CustomUser.objects.filter(groups__name__in=['Coordenador', 'Gerente', 'Usuário']).distinct().prefetch_related('groups')
        # if user.groups.filter(name='Gerente').exists():
        #     return CustomUser.objects.filter(groups__name__in=['Gerente', 'Usuário']).distinct().prefetch_related('groups')
        # return CustomUser.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['online_user_ids'] = get_online_user_ids()
        return context

class UserCreateView(ManagerialRoleRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('core:user_management')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['requesting_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, f"Usuário {form.cleaned_data.get('username')} criado com sucesso!")
        return super().form_valid(form)

class UserUpdateView(ManagerialRoleRequiredMixin, UpdateView):
    model = CustomUser
    form_class = AdminUserUpdateForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('core:user_management')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not user_can_manage_other(self.request.user, obj):
            raise PermissionDenied("Você não tem permissão para editar este usuário.")
        return obj

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['requesting_user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Usuário atualizado com sucesso!")
        return super().form_valid(form)

class UserDeleteView(ManagerialRoleRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'user_confirm_delete.html'
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
    Lista pública de todos os usuários ATIVOS do sistema.
    """
    model = CustomUser
    template_name = 'user_list.html'
    context_object_name = 'users'
    queryset = CustomUser.objects.filter(is_active=True).prefetch_related('groups')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['online_user_ids'] = get_online_user_ids()
        return context

class UserProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user_profile.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.get_object()
        all_applications = Application.objects.prefetch_related('modules').order_by('name')
        user_module_ids = set(profile_user.modules.values_list('id', flat=True))

        context['all_applications'] = all_applications
        context['user_module_ids'] = user_module_ids
        context['online_user_ids'] = get_online_user_ids()
        
        return context

@login_required
def self_profile_update_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('base:user_profile', pk=request.user.pk)
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'profile_form.html', {'form': form})

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('core:user_list')

    def form_valid(self, form):
        messages.success(self.request, "Sua senha foi alterada com sucesso!")
        return super().form_valid(form)

# --- Views de Gerenciamento de Acesso às Aplicações ---
@login_required
def manage_user_access_view(request, pk):
    target_user = get_object_or_404(CustomUser, pk=pk)

    if not user_can_manage_other(request.user, target_user):
        messages.error(request, "Você não tem permissão para gerenciar os acessos deste usuário.")
        return redirect('core:user_management')
    
    if request.method == 'POST':
        module_ids = request.POST.getlist('modules')
        target_user.modules.set(module_ids)
        messages.success(request, f"Acessos do usuário {target_user.username} atualizados.")
        return redirect('core:user_management')

    applications = Application.objects.prefetch_related('modules').all()
    user_module_ids = set(target_user.modules.values_list('id', flat=True))

    context = {
        'target_user': target_user,
        'applications': applications,
        'user_module_ids': user_module_ids
    }
    return render(request, 'manage_user_access.html', context)

@login_required
def user_password_change_view(request, pk):
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

    return render(request, 'admin_password_change_form.html', {
        'form': form,
        'target_user': target_user
    })

# NOVA VIEW PARA O TEMA
@login_required
@require_POST
def set_user_theme(request):
    """
    Recebe uma requisição POST com a escolha de tema do usuário
    e a salva no seu perfil.
    """
    try:
        data = json.loads(request.body)
        theme = data.get('theme')

        if theme in ['light', 'dark']:
            user = request.user
            user.theme = theme
            user.save(update_fields=['theme'])
            return JsonResponse({'status': 'ok', 'message': 'Tema atualizado com sucesso.'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Tema inválido.'}, status=400)
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'status': 'error', 'message': 'Requisição inválida.'}, status=400)