from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .models import Servidor

class formulario_añadir_nuevo_servidor(forms.Form):
    # template_name_p='../../../../web_hosting_automatico/dashboard/static/dashboard/add_new_server_as_p.html' #<- no vale
    # template_name="dashboard/add_new_server_as_p.html" <- problema con la ruta, ya se ha copiado y adaptado la template en el index.html
    name = forms.CharField(
        max_length=2048,
        min_length=10,
        strip=False,
        empty_value='',
        required=True, 
        widget=forms.TextInput(attrs={'autocomplete':'off', 'class':'form-control'}),
        label='Nombre del servidor', 
        initial='www.ejemplo.es',
        # help_text='Aquí debes introducir el nombre de la URL que quieres que tu sitio adopte', se puede introducir pero se debe adaptar el html
        error_messages={
            'required' : 'Este campo es requerido',
            'max_length' : 'WOW, donde vas? la longitud máxima es de 2048 caracteres, no lo digo yo, lo dicen los programadores de los buscadores',
            'min_length' : 'WOW, un poco corta tu tula no bro? al menos 3 cm',
            },
        show_hidden_initial=None,
        validators=[MaxLengthValidator(2048), MinLengthValidator(10)],
        localize=True,
        disabled=False,
        label_suffix='', # se aplica a vacío para que no muestre el ':' como sufijo del label
    )
    cms_type = forms.ChoiceField(
        choices=Servidor.CMS, 
        required=True, 
        widget=forms.Select(attrs={'class':'form-select mt-3'}),
        label='Tipo de CMS',
        initial=None, # por defecto coge el primero
        help_text='',
        error_messages={
            'required' : 'Este campo es requerido',
            'invalid_choice' : 'Jaja pillín, creías que podrías hackear este formulario'
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
            'invalid_choice' : 'Jaja pillín, creías que podrías hackear este formulario'
            }, 
        show_hidden_initial=None,
        validators=[],
        localize=True,
        disabled=False,
        label_suffix='',
    )
    cpanel_password = forms.CharField(
        max_length=20, # mirar .models
        min_length=8,
        strip=False,
        empty_value='',
        required=True,
        widget=forms.PasswordInput(attrs={'class':'form-control'}),
        label='Contraseña del panel',
        initial='',
        help_text='',
        error_messages={
            'required' : 'Este campo es requerido',
            'max_length' : 'WOW, donde vas? la longitud máxima es de 2048 caracteres, no lo digo yo, lo dicen los programadores de los buscadores',
            'min_length' : 'WOW, un poco corta tu tula no bro? al menos 3 cm',
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
        # import re
        name = self.data['name']
        # if re.match(r'^www.[].[es|com|au]',name) :
        #     pass
        existing_names = Servidor.objects.filter(name__exact=name).exists()
        if existing_names :
            self.add_error('name', 'Este nombre ya existe')
        return self

    def validate(self):
        self = self.name_is_valid()
        return self