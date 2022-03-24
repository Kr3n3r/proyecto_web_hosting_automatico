from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .models import Servidor

cms_type_choices = []
for item in Servidor.CMS:
    item = list(item)
    cms_type_choices += item

server_types_choices = []
for item in Servidor.SERVER_TYPES : 
    item = list(item)
    server_types_choices += item
class formulario_añadir_nuevo_servidor(forms.Form):
    name = forms.CharField(label='Nombre del servidor:', min_length=10 ,max_length=2048, required=True, validators=[MaxLengthValidator(2048), MinLengthValidator(10)])
    cms_type = forms.ChoiceField(
        label='Tipo de CMS', 
        choices=Servidor.CMS, 
        required=True, 
        label_suffix='', 
        error_messages={
            'required' : 'Este campo es requerido',
            'invalid_choice' : 'La opción seleccionada es inválida'
            }, 
        validators=[]
    )
    server_type = forms.ChoiceField(
        choices=Servidor.SERVER_TYPES, 
        required=True,
        error_messages={
            'required' : 'Este campo es requerido',
            'invalid_choice' : 'La opción seleccionada es inválida'
        },
        validators=[])
    cpanel_password = forms.CharField(
        widget=forms.PasswordInput, 
        required=True,
        min_length=8,
        max_length=20, # mirar .models
        validators=[MaxLengthValidator(20), MinLengthValidator(8)]
    )
    widgets = {
        'cpanel_password' : forms.PasswordInput(),
    }