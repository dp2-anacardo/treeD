from django import forms
from main.models import Perfil, DirecPerfil
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
import re

class DateInput(forms.DateInput):
    input_type = 'date'

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.jpeg', '.bmp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Los archivos deben ser imagenes .jpg, .png, .jpeg o .bmp')
        
class EditarUsernameForm(forms.ModelForm):
    username = forms.CharField(label="Username", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))

    class Meta:
        model = User
        fields = ('username', )

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get("username")

        if len(username) < 6:
            msg = "El nombre de usuario debe tener al menos 6 caracteres"
            raise ValidationError({'username': [msg, ]})

        if not re.match("^[A-Za-z0-9]*$", username):
            msg = "El nombre de usuario solo puede contener letras y numeros"
            raise ValidationError({'username': [msg, ]})

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            msg = "El nombre de usuario ya esta en uso"
            raise ValidationError({'username': [msg, ]})


class EditarPasswordForm(forms.Form):

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    check_pw = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

    def clean(self):
        cleaned_data = self.cleaned_data
        password = cleaned_data.get("password")
        check_pw = cleaned_data.get("check_pw")
        if password != check_pw:
            msg = "La contraseña no coincide"
            raise ValidationError({'password': [msg, ]})

        if len(password) < 8:
            msg = "La contraseña debe tener al menos 8 caracteres"
            raise ValidationError({'password': [msg, ]})

        if not re.match("^[A-Za-z0-9]*$", password):
            msg = "La contraseña solo puede contener letras y numeros"
            raise ValidationError({'password': [msg, ]})

        if not any(x.isupper() for x in password):
            msg = "La contraseña debe contener al menos una mayuscula"
            raise ValidationError({'password': [msg, ]})


class EditarPerfilForm(forms.ModelForm):

    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras y símbolos"),
        'apellidos_letters': ("Los apellidos solo pueden contener letras y símbolos"),
    }

    nombre = forms.CharField(label="Nombre", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Nombre'}))
    apellidos = forms.CharField(label="Apellidos", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Apellidos'}))
    email = forms.CharField(label="Email", widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))
    descripcion = forms.CharField(label="Descripción", required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Descripcion', 'rows': 4}))
    imagen = forms.ImageField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': False, 'class': 'form-control-file'}),
            validators=[validate_file_extension]
    )

    class Meta:
        model = Perfil
        fields = (
            "nombre",
            "apellidos",
            "descripcion",
            "imagen",
            "email",
        )

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", nombre):
            raise forms.ValidationError(
                self.error_messages['nombre_letters'],
                code='nombre_letters',
            )
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", apellidos):
            raise forms.ValidationError(
                self.error_messages['apellidos_letters'],
                code='apellidos_letters',
            )
        return apellidos

    def __init__(self, *args, **kwargs):
        super(EditarPerfilForm, self).__init__(*args, **kwargs)
        self.fields['descripcion'].required = False
        self.fields['imagen'].required = False


class AñadirDirecPerfilForm(forms.Form):
    direccion = forms.CharField(label="Direccion principal", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Ciudad, Calle Nº, CP'}))

class DireccionForm(forms.Form):

    direccion = forms.ModelChoiceField(
        label='', queryset=DirecPerfil.objects.all())


class ImagenForm(forms.Form):
    imagen = forms.ImageField(required=False,
                              widget=forms.ClearableFileInput(
                                  attrs={'class': 'form-control-file'}),
                                  validators=[validate_file_extension])


class PerfilForm(forms.ModelForm):
    error_messages = {
        'nombre_letters': ("El nombre solo puede contener letras y símbolos"),
        'apellidos_letters': ("Los apellidos solo pueden contener letras y símbolos"),
    }

    class Meta:
        model = Perfil
        fields = {
            'nombre',
            'apellidos',
            'email',
            'descripcion',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Descripción', 'rows': 4}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", nombre):
            raise forms.ValidationError(
                self.error_messages['nombre_letters'],
                code='nombre_letters',
            )
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')

        if not re.match("^[A-Za-zÀ-ÿ\u00f1\u00d1\u0020]*$", apellidos):
            raise forms.ValidationError(
                self.error_messages['apellidos_letters'],
                code='apellidos_letters',
            )
        return apellidos


class DirecPerfilForm(forms.ModelForm):
    class Meta:
        model = DirecPerfil
        fields = {
            'direccion',
        }
        widgets = {
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad, Calle Nº, CP'}),
        }


class UserForm(forms.ModelForm):

    error_messages = {
        'password_mismatch': ("Las contraseñas no coinciden"),
        'username_exists': ("Ya existe ese nombre de usuario"),
        'password_short': ("La contraseña debe tener al menos 8 caracteres"),
        'password_letters': ("La contraseña solo puede contener letras y números"),
        'password_capital': ("La contraseña debe tener al menos una mayúscula"),
        'username_short': ("El nombre de usuario debe tener al menos 6 caracteres"),
        'username_letters': ("El nombre de usuario solo puede contener letras y numeros"),
    }

    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control', 'placeholder': 'Confirme su contraseña'}),
                                help_text=("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de Usuario'})
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        if len(password1) < 8:
            raise forms.ValidationError(
                self.error_messages['password_short'],
                code='password_short',
            )

        if not re.match("^[A-Za-z0-9]*$", password1):
            raise forms.ValidationError(
                self.error_messages['password_letters'],
                code='password_letters',
            )

        if not any(x.isupper() for x in password1):
            raise forms.ValidationError(
                self.error_messages['password_capital'],
                code='password_capital',
            )
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 6:
            raise forms.ValidationError(
                self.error_messages['username_short'],
                code='username_short',
            )

        if not re.match("^[A-Za-z0-9]*$", username):
            raise forms.ValidationError(
                self.error_messages['username_letters'],
                code='username_letters',
            )

        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(
                self.error_messages['username_exists'],
                code='username_exists',
            )
        return username

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
