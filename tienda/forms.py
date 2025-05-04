from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django import forms
import uuid

class CustomUserCreationForm(UserCreationForm):
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