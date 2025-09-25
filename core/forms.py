from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.models import Group
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Formulário para criação de usuários por administradores/gerentes.
    Permite definir o grupo do novo usuário.
    """
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'profile_picture', 'allowed_ip_address')
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'profile_picture': 'Foto de Perfil',
            'allowed_ip_address': 'IP de Acesso Permitido',
        }

    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    def __init__(self, *args, **kwargs):
        self.requesting_user = kwargs.pop('requesting_user', None)
        super().__init__(*args, **kwargs)
        
        if self.requesting_user:
            if self.requesting_user.groups.filter(name='Coordenador').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Gerente', 'Usuário'])
            elif self.requesting_user.groups.filter(name='Gerente').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Usuário'])

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.help_text = None # Remove o texto de ajuda padrão do Django

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
        labels = {
            'username': 'Nome de Usuário',
            'email': 'E-mail',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'profile_picture': 'Foto de Perfil',
            'allowed_ip_address': 'IP de Acesso Permitido',
            'is_active': 'Ativo',
        }

    def __init__(self, *args, **kwargs):
        self.requesting_user = kwargs.pop('requesting_user', None)
        super().__init__(*args, **kwargs)
        
        if self.instance.pk and self.instance.groups.exists():
            self.fields['group'].initial = self.instance.groups.first()

        if self.requesting_user:
            if self.requesting_user.groups.filter(name='Coordenador').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Gerente', 'Usuário'])
            elif self.requesting_user.groups.filter(name='Gerente').exists():
                self.fields['group'].queryset = Group.objects.filter(name__in=['Usuário'])
        
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            group = self.cleaned_data.get('group')
            user.groups.set([group])
        return user

class CustomUserChangeForm(UserChangeForm):
    """
    Formulário para o próprio usuário editar seu perfil.
    Remove campos sensíveis.
    """
    password = None
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'profile_picture')
        labels = {
            'email': 'E-mail',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'profile_picture': 'Foto de Perfil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = "Senha antiga"
        self.fields['new_password1'].label = "Nova senha"
        self.fields['new_password2'].label = "Confirmação da nova senha"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            field.help_text = None

class AdminPasswordChangeForm(SetPasswordForm):
    """
    Formulário para um administrador alterar a senha de outro usuário.
    Não requer a senha antiga.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label = "Nova senha"
        self.fields['new_password2'].label = "Confirmação da nova senha"
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})