from django import forms
from .models import Servidor

class formulario_añadir_nuevo_servidor(forms.Form):
    name = forms.CharField(label='', max_length=2048, required=True)
    cms_type = forms.MultipleChoiceField(choices=Servidor.cms_type(1), required=True)
    server_type = forms.ChoiceField(choices=Servidor.SERVER_TYPES(1), required=True)
    cpanel_password = forms.PasswordInput()