# --- Arquivo de URLs do App: urls.py ---
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    login_view,
    logout_view,
    home,
    settings,
    user_profile,
    UserManagementView,
    UserListView,
    UserProfileView,
    self_profile_update_view,
    CustomPasswordChangeView,
    UserCreateView,
    UserUpdateView,
    manage_user_access_view,
    user_password_change_view,
    UserDeleteView,
    set_user_theme,
)

app_name = 'base'

urlpatterns = [
    # Autenticação
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    
    # Tela Inicial
    path('', home, name='home'),

    # Configurações
    path('settings', settings, name='settigns'),
    path('settings/set-theme/', set_user_theme, name='set_theme'),
    
    # Gerenciamento de Usuários (Hierárquico)
    path('management/users/', UserManagementView.as_view(), name='user_management'),
    path('management/users/create/', UserCreateView.as_view(), name='user_create'),
    path('management/users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('management/users/access/<int:pk>/', manage_user_access_view, name='manage_user_access'),
    path('management/users/password-change/<int:pk>/', user_password_change_view, name='admin_password_change'),
    path('management/users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    
    # Perfil e Listas Públicas
    path('<str:username>', user_profile, name='user_profile'),
    path('profile/edit/', self_profile_update_view, name='self_profile_update'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    
    
]