from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Comuna, Region, Producto, Categoria
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django import forms
import uuid

class ClienteCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu correo electrónico'}))
    password1 = forms.CharField( label="Contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Introduce tu contraseña'}))
    password2 = forms.CharField(label="Confirma tu contraseña", widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirma tu contraseña'}))
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email
    
    def clean_password(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = str(uuid.uuid4())[:30]  # Generamos un username único
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    
class EmailLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Introduce tu correo electrónico'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Introduce tu contraseña'
    }))

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Correo electrónico no registrado')

        user = authenticate(username=user.username, password=password)
        if not user:
            raise forms.ValidationError('Contraseña incorrecta')

        self.user = user
        return self.cleaned_data
    
User = get_user_model()

class DatosUsuarioForm(forms.Form):
    nombre = forms.CharField(max_length=150, required=True, label='Nombre')
    primer_apellido = forms.CharField(max_length=150, required=True, label='Primer apellido')
    segundo_apellido = forms.CharField(max_length=150, required=False, label='Segundo apellido')
    telefono = forms.CharField(max_length=20, required=True, label='Teléfono')
    calle = forms.CharField(max_length=255, required=True, label='Calle')
    numero = forms.CharField(max_length=20, required=True, label='Número')
    region = forms.ModelChoiceField(
        queryset=Region.objects.all(),
        required=True,
        label='Región'
    )
    comuna = forms.ModelChoiceField(
        queryset=Comuna.objects.none(),
        required=True,
        label='Comuna'
    )

    def __init__(self, *args, **kwargs):
        region_id = kwargs.pop('region_id', None)
        super().__init__(*args, **kwargs)

        if region_id:
            try:
                region_id = int(region_id)
                self.fields['comuna'].queryset = Comuna.objects.filter(region_id=region_id)
            except (ValueError, TypeError):
                self.fields['comuna'].queryset = Comuna.objects.none()
        else:
            self.fields['comuna'].queryset = Comuna.objects.none()


GRUPOS_VISIBLES = ['Administrador', 'Vendedor', 'Bodeguero', 'Contador']

class TrabajadorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'groups']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.filter(name__in=GRUPOS_VISIBLES)
        self.fields['groups'].label = "Rol"

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'groups']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.filter(name__in=GRUPOS_VISIBLES)
        self.fields['groups'].label = "Rol"

class ProductoForm(forms.ModelForm):
    nueva_categoria = forms.CharField(
        required=False,
        label="Nueva categoría",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'stock',
            'precio_venta', 'precio_compra',
            'categoria', 'unidad_medida', 'imagen'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select', 'id': 'id_categoria'}),
            'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }