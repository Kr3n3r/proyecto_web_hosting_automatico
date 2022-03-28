from this import d
from threading import local
from django import forms
from django.core.validators import MaxLengthValidator, MinLengthValidator
from .models import Servidor

class formulario_añadir_nuevo_servidor(forms.Form):
    # template_name_p='../../../../web_hosting_automatico/dashboard/static/dashboard/add_new_server_as_p.html' #<- no vale
    # template_name="dashboard/add_new_server_as_p.html" <- problema con la ruta, ya se ha copiado y adaptado la template en el index.html
    name = forms.CharField(
        label='Nombre del servidor:',
        initial='www.webejemplo.es',
        min_length=10,
        max_length=2048, 
        required=True, 
        validators=[
            MaxLengthValidator(2048), MinLengthValidator(10)
            ])
    cms_type = forms.ChoiceField(
        label='Tipo de CMS',
        # initial=0, # se hace con la intención de añadir una opción por defecto que no sea seleccionable 
        # show_hidden_initial=True,
        choices=Servidor.CMS, 
        required=True, 
        label_suffix='', 
        error_messages={
            'required' : 'Jaja, creías que me ibas a joder la query por no introducir estos datos no pedazo de puto?',
            'invalid_choice' : 'Jaja pillín, creías que podrías hackear este formulario'
            }, 
        validators=[]
    )
    server_type = forms.ChoiceField(
        choices=Servidor.SERVER_TYPES, 
        required=True,
        error_messages={
            'required' : 'Jaja, creías que me ibas a joder la query por no introducir estos datos no pedazo de puto?',
            'invalid_choice' : 'Jaja pillín, creías que podrías hackear este formulario'
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
    
    def name_is_valid(self): # thats not the way. Habría que encontrar una forma de hacer más genérico esto
        name = self.data['name']
        results = Servidor.objects.filter(name=name)
        if results.count() != 0 :
            self.errors['name'] = ['The name is not UNIQUE']
        return self
        