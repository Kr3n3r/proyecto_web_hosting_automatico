from django.test import TestCase
from .models import Servidor, Usuario


# Create your tests here.
# aquí voy a crear las pruebas unitarias para ciertos aspectos de esta aplicación
# ie : probar el display de errores de validación, etc

class Test_Case_Formulario_añadir_nuevo_servidor(TestCase) :
    def test_errores(self):
        from dashboard.forms import formulario_añadir_nuevo_servidor
        from dashboard.models import Servidor,Usuario
        usuario = Usuario(
            name='Usuarios',
            surname='de prueba',
            DNI='12345678A',
            email='prueba@prueba.prueba',
            username='prueba',
            password='prueba')
        usuario.save()
        servidor_existente = Servidor(
            user_admin=usuario,
            name='www.alejandro.com',
            cms_type='Wordpress',
            server_type='Standart',
            public_ip='1.2.3.4',
            cpanel_password='12345678')
        servidor_existente.save()
        form = formulario_añadir_nuevo_servidor({
            'name' : 'www.alejandro.com',
            'cms_type' : 1,
            'server_type' : 1,
            'cpanel_password' : '12345678',
        })
        form.validate()
        self.assertEqual(len(form.errors), 1)
