from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Servicio, PerfilUsuario


class ServicioForm(forms.ModelForm):
    class Meta:
        model  = Servicio
        fields = ['nombre', 'descripcion', 'precio', 'categoria', 'activo']
        widgets = {
            'nombre':      forms.TextInput(attrs={'class': 'form-control', 'maxlength': '60', 'placeholder': 'Ej: Renta del salón'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'maxlength': '250', 'rows': '4', 'placeholder': 'Describe brevemente el servicio...'}),
            'precio':      forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01', 'placeholder': '0.00'}),
            'categoria':   forms.Select(attrs={'class': 'form-control'}),
            'activo':      forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        v = self.cleaned_data.get('nombre', '').strip()
        if len(v) < 3:
            raise forms.ValidationError('El nombre debe tener al menos 3 caracteres.')
        return v

    def clean_descripcion(self):
        v = self.cleaned_data.get('descripcion', '').strip()
        if len(v) < 10:
            raise forms.ValidationError('La descripción debe tener al menos 10 caracteres.')
        return v

    def clean_precio(self):
        v = self.cleaned_data.get('precio')
        if v is not None and v <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return v


class RegistroUsuarioForm(UserCreationForm):
    email    = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '443 000 0000'}))
    rol      = forms.ChoiceField(choices=PerfilUsuario.ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario123'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            PerfilUsuario.objects.create(
                usuario  = user,
                rol      = self.cleaned_data['rol'],
                telefono = self.cleaned_data.get('telefono', ''),
            )
        return user


class RegistroClienteForm(UserCreationForm):
    email    = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}))
    telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '443 000 0000'}))

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario123'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ya existe una cuenta con ese correo.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ModificarUsuarioForm(forms.ModelForm):
    telefono = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rol      = forms.ChoiceField(choices=PerfilUsuario.ROLES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance and hasattr(instance, 'perfil'):
            self.fields['rol'].initial      = instance.perfil.rol
            self.fields['telefono'].initial = instance.perfil.telefono

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            perfil, _ = PerfilUsuario.objects.get_or_create(usuario=user)
            perfil.rol      = self.cleaned_data['rol']
            perfil.telefono = self.cleaned_data.get('telefono', '')
            perfil.save()
        return user
