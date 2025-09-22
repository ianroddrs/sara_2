# --- Arquivo de URLs do App: core/urls.py ---
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    CustomLoginView,
    UserManagementView,
    UserListView,
    UserProfileView,
    self_profile_update_view,
    CustomPasswordChangeView,
    UserCreateView,
    UserUpdateView,
    manage_user_access_view,
    module_placeholder_view,
    user_password_change_view
)

app_name = 'core'

urlpatterns = [
    # Autenticação
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='core:login'), name='logout'),
    
    # Gerenciamento de Usuários (Hierárquico)
    path('management/users/', UserManagementView.as_view(), name='user_management'),
    path('management/users/create/', UserCreateView.as_view(), name='user_create'),
    path('management/users/edit/<int:pk>/', UserUpdateView.as_view(), name='user_edit'),
    path('management/users/access/<int:pk>/', manage_user_access_view, name='manage_user_access'),
    path('management/users/password-change/<int:pk>/', user_password_change_view, name='admin_password_change'),
    
    # Perfil e Listas Públicas
    path('', UserListView.as_view(), name='user_list'), # Home page
    path('users/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', self_profile_update_view, name='self_profile_update'),
    path('profile/change-password/', CustomPasswordChangeView.as_view(), name='password_change'),
    
    # Placeholders dos Módulos
    path('module/<str:module_name>/', module_placeholder_view, name='module_placeholder'),
]