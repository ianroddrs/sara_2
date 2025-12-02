from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import LoginView as BaseLoginView, PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash, authenticate
from django.contrib.auth.models import Group
from .models import Application
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    AdminUserUpdateForm,
    CustomPasswordChangeForm,
    AdminPasswordChangeForm
)
from .utils import user_can_manage_other
from .decorators import secure_module_access

CustomUser = get_user_model()

@require_POST
def login_view(request):
    form = AuthenticationForm(request, data=request.POST)
    
    if form.is_valid():
        user = form.get_user()

        # Verificação de IP (Lógica mantida)
        if hasattr(user, 'allowed_ip_address') and user.allowed_ip_address:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            request_ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

            if user.allowed_ip_address != request_ip:
                return JsonResponse(
                    {"message": "Acesso negado. Endereço de IP não autorizado."}, 
                    status=403
                )
        
        login(request, user)
        next_url = request.POST.get('next') or reverse('base:home')
        
        return JsonResponse({
            "message": "Login realizado com sucesso!", 
            "redirect_url": next_url
        }, status=200)

    else:
        return JsonResponse(
            {"message": "Acesso negado. Usuário ou senha incorreto."}, 
            status=401
        )

@require_POST
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({
            'message': 'Logout realizado com sucesso.'
        }, status=200)


def home(request):
    users = CustomUser.objects.filter(is_active=True).prefetch_related('groups')
    applications = Application.objects.all() 
    context = {
        
    }
    
    return render(request, "base/home.html", context)

def settings(request):
    context = {}
    return render(request, 'base/settings.html', context)

@login_required
def self_profile_update_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('base:user_profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'settings/profile_form.html', {'form': form})

@login_required
def self_password_update_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('base:user_profile', username=request.user.username)

# --- Mixins de Permissão Hierárquica ---
class ManagerialRoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name__in=['Administrador', 'Coordenador', 'Gerente']).exists()

    def handle_no_permission(self):
        messages.error(self.request, "Você não tem permissão para acessar esta página.")
        return redirect('base:home')

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

class UserCreateView(ManagerialRoleRequiredMixin, CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'settings/profile_form.html'
    success_url = reverse_lazy('base:user_management')

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
    template_name = 'settings/profile_form.html'
    success_url = reverse_lazy('base:user_management')
    
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
    success_url = reverse_lazy('base:user_management')

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
        
        return context

# --- Views de Gerenciamento de Acesso às Aplicações ---
@login_required
def manage_user_access_view(request, pk):
    target_user = get_object_or_404(CustomUser, pk=pk)

    if not user_can_manage_other(request.user, target_user):
        messages.error(request, "Você não tem permissão para gerenciar os acessos deste usuário.")
        return redirect('base:user_management')
    
    if request.method == 'POST':
        module_ids = request.POST.getlist('modules')
        target_user.modules.set(module_ids)
        messages.success(request, f"Acessos do usuário {target_user.username} atualizados.")
        return redirect('base:user_management')

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
        return redirect('base:user_management')

    if request.method == 'POST':
        form = AdminPasswordChangeForm(target_user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"A senha de {target_user.username} foi alterada com sucesso.")
            return redirect('base:user_management')
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