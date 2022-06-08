from django.test import TestCase
from .models import Servidor, Usuario


# Create your tests here.
# aquí voy a crear las pruebas unitarias para ciertos aspectos de esta aplicación
# ie : probar el display de errores de validación, etc

class Test_Case_Formulario_añadir_nuevo_servidor(TestCase) :
    def test_formulario_muestra_errores_nombre_duplicado(self):
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

class Test_Case_Renderizar_variables_ansible(TestCase) :
    from django.template.loader import render_to_string
    # rendered_text = render_to_string('dashboard/all', {
    #     'domain' : "ec2-13-41-80-204.eu-west-2.compute.amazonaws",
    #     'db_ip' : "dbprueba.cfsjy7ys8tan.eu-west-2.rds.amazonaws.com",
    #     'mysql_db' : "test_mediawiki_db",
    #     "mysql_user" : "admin",
    #     "mysql_password" : "1qaz.WSX",
    #     "mysql_new_user" : "test_mediawiki_user",
    #     "mysql_new_password" : "test_mediawiki_password",
    #     "site_name" : "La wiki de Prueba",
    #     "admin_user" : "admin",
    #     "admin_password" : "admin",
    #     "name_user" : "administrador",
    #     "surname_user" : "admin",
    #     "server" : "Prueba",
    #     })
    # rendered_text = render_to_string('dashboard/all', {
    #     'domain' : "ec2-3-8-135-76.eu-west-2.compute.amazonaws.com",
    #     'db_ip' : "dbprueba.cfsjy7ys8tan.eu-west-2.rds.amazonaws.com",
    #     'mysql_db' : "test_prestashop_db",
    #     "mysql_user" : "admin",
    #     "mysql_password" : "1qaz.WSX",
    #     "mysql_new_user" : "test_prestashop_user",
    #     "mysql_new_password" : "test_prestashop_password",
    #     "site_name" : "La tienda de prueba",
    #     "admin_user" : "admin",
    #     "admin_password" : "Prueba_1",
    #     "name_user" : "administrador",
    #     "surname_user" : "admin",
    #     "server" : "Prueba",
    #     })
    # rendered_text = render_to_string('dashboard/all.wordpress', {
    #     'db_ip' : "dbprueba.cfsjy7ys8tan.eu-west-2.rds.amazonaws.com",
    #     "mysql_user" : "admin",
    #     "mysql_password" : "1qaz.WSX",
    #     'mysql_db' : "test_wordpress_db",
    #     "mysql_new_user" : "test_wordpress_user",
    #     "mysql_new_password" : "test_wordpress_password",
    #     'http_host' : "ec2-3-8-135-76.eu-west-2.compute.amazonaws.com",
    #     'http_conf' : "ec2-3-8-135-76.eu-west-2.compute.amazonaws.com.conf",
    #     })
    rendered_text=None
    print(rendered_text)

class Test_Case_Renderizar_variables_terraform(TestCase) :
    from django.template.loader import render_to_string
    rendered_text = render_to_string('dashboard/terraform_template', {
        'sshkey' : 'AAAAB3NzaC1yc2EAAAADAQABAAABAQCC4+glaxVjgpMgSxYqDz19TQTnxbFKy60SdcQDtySO8GiCJtvIyWtjd1IJPJxWYavNuG+RB2SH7wTDtKuYHXp4ZHAtcqS410Y4sTRf1ehASQRkph43tn4fDubYwV7OpspV0tdJNsCpBlTQOdra1NEG1zuCoAuircH/bXWCO+fev1G2eAmHN06G3jxw1zsLHrf/m2xRqIDYhkhKChWP0CBGz5tiuj4TKsArg/KQJWnTToKDbEXNQ67AHLZfydNAogZGwgGSLm+M4PVlTqhRV37PXq0W/aqoH7NQ2MiUIiK0HaS6+wKoIDKd6RWZ1vDhcAsyrK4uUDEnq5mTYs43k/bb',
        'name' : 'Prueba',
        'db_name' : 'Test',
        'db_password' : '1qaz.WSX',
        'db_user' : 'root',
        'db_instance_name' : 'PruebaBD',
        })
    print(rendered_text)