# --- Arquivo de URLs do App: urls.py ---
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home,
    login_api,
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
    path('api/login/', login_api, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='base:home'), name='logout'),
    
    # Tela Inicial
    path('', home, name='home'),
    
    # Gerenciamento de Usuários (Hierárquico)
    path('management/users/', UserManagementView.as_view(), name='user_management'),
    path('management/users/create/', UserCreateView.as_view(), name='user_create'),
    path('management/users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('management/users/access/<int:pk>/', manage_user_access_view, name='manage_user_access'),
    path('management/users/password-change/<int:pk>/', user_password_change_view, name='admin_password_change'),
    path('management/users/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    
    # Perfil e Listas Públicas
    path('users/', UserListView.as_view(), name='user_list'), # Home page
    path('users/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', self_profile_update_view, name='self_profile_update'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    
    # NOVA URL PARA O TEMA
    path('set-theme/', set_user_theme, name='set_theme'),
    
]