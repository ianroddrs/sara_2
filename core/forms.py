from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import Group
from .models import CustomUser, Application, UserApplicationAccess

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário para criação de usuários por administradores/gerentes.
    Permite definir o grupo do novo usuário.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'allowed_ip_address')

    # Campo para selecionar o grupo do usuário
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    def __init__(self, *args, **kwargs):
        self.requesting_user = kwargs.pop('requesting_user', None)
        super().__init__(*args, **kwargs)
        # Filtra os grupos que o usuário logado pode atribuir
        if self.requesting_user:
            if self.requesting_user.groups.filter(name='Coordenador').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Gerente', 'Usuário'])
            elif self.requesting_user.groups.filter(name='Gerente').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Usuário'])
            # Administrador vê todos os grupos por padrão

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = self.cleaned_data.get('group')
            user.groups.add(group)
        return user

class AdminUserUpdateForm(forms.ModelForm):
    """
    Formulário para que usuários com poder hierárquico possam
    editar outros usuários.
    """
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'allowed_ip_address', 'is_active')

    def __init__(self, *args, **kwargs):
        self.requesting_user = kwargs.pop('requesting_user', None)
        super().__init__(*args, **kwargs)
        
        # Define o grupo inicial no formulário
        if self.instance.pk and self.instance.groups.exists():
            self.fields['group'].initial = self.instance.groups.first()

        # Filtra os grupos que podem ser atribuídos
        if self.requesting_user:
            if self.requesting_user.groups.filter(name='Coordenador').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Gerente', 'Usuário'])
            elif self.requesting_user.groups.filter(name='Gerente').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Usuário'])

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = self.cleaned_data.get('group')
            user.groups.set([group]) # `set` limpa os grupos antigos e adiciona o novo
        return user


class CustomUserChangeForm(UserChangeForm):
    """
    Formulário para o próprio usuário editar seu perfil.
    Remove campos sensíveis.
    """
    password = None # Remove o campo de senha
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'profile_picture')

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class AdminPasswordChangeForm(SetPasswordForm):
    """
    Formulário para um administrador alterar a senha de outro usuário.
    Não requer a senha antiga.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class UserAccessForm(forms.Form):
    """
    Formulário para gerenciar o acesso de um usuário às aplicações.
    """
    applications = forms.ModelMultipleChoiceField(
        queryset=Application.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Aplicações com Acesso Permitido"
    )

    def __init__(self, *args, **kwargs):
        user_instance = kwargs.pop('user_instance', None)
        super().__init__(*args, **kwargs)
        if user_instance:
            # Pré-seleciona as aplicações que o usuário já tem acesso
            self.fields['applications'].initial = Application.objects.filter(
                userapplicationaccess__user=user_instance,
                userapplicationaccess__has_access=True
            )