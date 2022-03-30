from django.test import TestCase
from .models import Servidor, Usuario
from .forms import formulario_añadir_nuevo_servidor

# Create your tests here.
# aquí voy a crear las pruebas unitarias para ciertos aspectos de esta aplicación
# ie : probar el display de errores de validación, etc

class Test_Case_Formulario_añadir_nuevo_servidor(TestCase) :
    def test_errores(self):
        form = formulario_añadir_nuevo_servidor({
            'name' : 'www.alejandro.com',
            'cms_type' : 1,
            'server_type' : 1,
            'cpanel_password' : '12345678',
        })
        form.validate()
        self.assertEqual(len(form.errors), 1)
