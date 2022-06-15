from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .models import Servidor

class formulario_añadir_nuevo_servidor(forms.Form):
    name = forms.CharField(
        max_length=2048,
        min_length=10,
        strip=False,
        empty_value='',
        required=True, 
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'}),
        label='URL de la web', 
        initial='www.miprimeraweb.es',
        # help_text='Aquí debes introducir el nombre de la URL que quieres que tu sitio adopte', se puede introducir pero se debe adaptar el html
        error_messages={
            'required' : 'Este campo es requerido',
            'max_length' : 'La longitud máxima es de 2048 caracteres',
            'min_length' : 'La longitud mínima es de 10 caracteres',
            },
        show_hidden_initial=None,
        validators=[MaxLengthValidator(2048), MinLengthValidator(10)],
        localize=True,
        disabled=False,
        label_suffix='',
    )
    web_name = forms.CharField(
        max_length=2048,
        min_length=None,
        strip=False,
        empty_value='',
        required=True, 
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'}),
        label='Nombre de la web', 
        initial='Mi Primera Web',
        # help_text='Aquí debes introducir el nombre de la URL que quieres que tu sitio adopte', se puede introducir pero se debe adaptar el html
        error_messages={
            'required' : 'Este campo es requerido',
            'max_length' : 'La longitud máxima es de 2048 caracteres',
            },
        show_hidden_initial=None,
        validators=[MaxLengthValidator(2048), MinLengthValidator(10)],
        localize=True,
        disabled=False,
        label_suffix='', 
    )
    cms_type = forms.ChoiceField(
        choices=Servidor.CMS, 
        required=True, 
        widget=forms.Select(attrs={'class':'form-select mt-3'}),
        label='Tipo de web',
        initial=None,
        help_text='',
        error_messages={
            'required' : 'Este campo es requerido',
            'invalid_choice' : 'Esta es una opción no válida'
            }, 
        show_hidden_initial=None,
        validators=[],
        localize=True,
        disabled=False,
        label_suffix='',
    )
    server_type = forms.ChoiceField(
        choices=Servidor.SERVER_TYPES, 
        required=True, 
        widget=None,
        label='Tipo de servidor',
        initial=None, # por defecto coge el primero
        help_text='',
        error_messages={
            'required' : 'Este campo es requerido',
            'invalid_choice' : 'Esta es una opción no válida'
            }, 
        show_hidden_initial=None,
        validators=[],
        localize=True,
        disabled=False,
        label_suffix='',
    )
    logo = forms.ImageField(
        allow_empty_file=True,
        required=False,
        label='Logo de la web(Solo mediawiki)',
        label_suffix='',
    )
    admin_user = forms.CharField(
        required=True,
        label='Usuario administrador del sitio',
        localize=True,
        label_suffix='',
        disabled=False
    )
    admin_password = forms.CharField(
        max_length=20,
        min_length=8,
        strip=False,
        empty_value='',
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label='Contraseña del usuario adminstrador',
        initial='',
        help_text='',
        error_messages={
            'required' : 'Este campo es requerido',
            'max_length' : 'La longitud máxima es de 20 caracteres',
            'min_length' : 'La longitud mínima es de 8 caracteres',
            },
        show_hidden_initial=None,
        validators=[MaxLengthValidator(20), MinLengthValidator(8)],
        localize=True,
        disabled=False,
        label_suffix='',
    )
    widgets = {
        'cpanel_password' : forms.PasswordInput(),
    }
    
    def name_is_valid(self):
        name = self.data['name']
        existing_names = Servidor.objects.filter(id__exact=name).exists()
        if existing_names :
            self.add_error('name', 'Este nombre ya existe')
        return self

    def validate(self):
        self = self.name_is_valid()
        return self
