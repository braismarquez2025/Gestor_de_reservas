from django import forms
from datetime import datetime
from reserva.models import Reserva
from django.contrib.auth.models import User


class ReservaForm(forms.ModelForm):
    # Campo hora separado
    hora = forms.TimeField(
        label="Hora",
        widget=forms.TimeInput(format='%H:%M')
    )

    class Meta:
        model = Reserva
        fields = ['user', 'recurso', 'hora']


    def __init__(self, *args, **kwargs):
        # Recibimos la fecha del día seleccionado desde la vista
        self.selected_date = kwargs.pop('selected_date', None)
        super().__init__(*args, **kwargs)

    

class LoginForm(forms.Form):
    username = forms.CharField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password"]

    
    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data['password'])
        user.save()

        return user