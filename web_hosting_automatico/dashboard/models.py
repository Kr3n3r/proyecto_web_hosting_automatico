from django.db import models
from localflavor.es.models import ESIdentityCardNumberField

# Create your models here.
# Discusión sobre compartir o no modelos entre diferentes aplicaciones:
#   https://stackoverflow.com/questions/4137287/sharing-models-between-django-apps#:~:text=The%20answer%20is%20yes.,and%20not%20the%20other%20way.

# Se creará un modelo que guardará datos del usuario, como son 
#   nombre, apellidos, DNI, 
#   email, username, password
class Usuario(models.Model):
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=130)
    DNI = ESIdentityCardNumberField()
    email = models.EmailField(max_length=130)
    username = models.CharField(primary_key=True, max_length=255)
    password = models.CharField(max_length=20) 
    # hay que asegurar que la contraseña se encripta con algún tipo de hash en el formulario de registro
    
    def __str__(self):
        return self.username

# Se creará un modelo que guardará datos de los servidores, como son 
#   el nombre, tipo(WORDPRESS, DRUPAL, etc...), tipo de servidor(tarifa estandar, basic, premium), 
#   ip pública, password del panel
class Servidor(models.Model):
    CMS = [
        (1,'Wordpress'),
        (2,'Prestashop'),
        (3,'Mediawiki'),
    ]
    SERVER_TYPES = [
        (1,'Standart'),
        (2,'Basic'),
        (3,'Premium'),
    ]
    
    user_admin = models.ForeignKey(to='Usuario', on_delete=models.CASCADE, default='anybody')
    name = models.CharField(max_length=255)
    cms_type = models.CharField(choices=CMS, max_length=255)
    server_type = models.CharField(choices=SERVER_TYPES, max_length=255)
    public_ip = models.GenericIPAddressField(protocol='IPv4')

    def server_count(self, *args, **kwargs):
        count = Servidor.objects.filter(user_admin=self.user_admin)
        return count