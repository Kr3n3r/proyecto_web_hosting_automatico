from django.shortcuts import redirect, render
import django.contrib.auth
from re import *

# Create your views here.
from .models import Servidor, Usuario

app_name='dashboard'

def index(request):
    try:
        username = request.session['user']
    except:
        return redirect('login')
    server_list = Servidor.objects.filter(user_admin_id=username)
    return render(request, 'dashboard/index.html', {
        'user_name' : request.session['user'],
        'server_list' : server_list,
    })

def delete_item(request,id):
    server = Servidor.objects.get(id=id)
    if server.user_admin_id.pk == request.session['user'] :
        server.delete()
        return redirect('index')
    else:
        try:
            del request.session['user']
            request.session.modified = True
        except:
            return redirect('login')
    return redirect('login')

def logout(request):
    try:
        django.contrib.auth.logout(request)
        request.session.modified = True
    except:
        return redirect('login')
    return redirect('login')

from .forms import formulario_añadir_nuevo_servidor
from django.forms.utils import ErrorList
class div_invalidfeedback(ErrorList):  
    def __str__(self):
            return self.as_divs()
    def as_divs(self):
            if self: 
                return '<div class="invalid-feedback">%s</div>' % ''.join(['%s' % e for e in self])
            return ''

def generate_random_password():
    import string, random
    alphabets = list(string.ascii_letters)
    digits = list(string.digits)
    special_characters = list("!#$%^&*()")
    alphabets_count = 4
    digits_count = 4
    special_characters_count = 4
    password = []
    for i in range(alphabets_count):
        password.append(random.choice(alphabets))
    for i in range(digits_count):
        password.append(random.choice(digits))
    for i in range(special_characters_count):
        password.append(random.choice(special_characters))
    random.shuffle(password)
    return "".join(password)

def añadir_nuevo_servidor(request):
    try:
        username = request.session['user']
    except:
        return redirect('login')
    if request.method == 'POST' :
        form = formulario_añadir_nuevo_servidor(data=request.POST, error_class=div_invalidfeedback)
        form.validate()
        if form.is_valid() :
            from django.template.loader import render_to_string
            CMS = [('Wordpress','Wordpress'),('Prestashop','Prestashop'),('Mediawiki','Mediawiki'),]
            SERVER_TYPES = [('Standart','Standart'),('Basic','Basic'),('Premium','Premium'),]
            
            name = form.cleaned_data['name'].replace('.','_')
            web_name = form.cleaned_data['web_name']
            cms_type = form.cleaned_data['cms_type']
            server_type = form.cleaned_data['server_type']
            logo = None
            admin_user = form.cleaned_data['admin_user']
            admin_password = form.cleaned_data['admin_password']
            Admin = Usuario.objects.get(username=request.session['user'])
            
            db_password = generate_random_password()
            db_name = cms_type.lower() + "_db"
            db_user = cms_type.lower() + "_user"
            
            rendered_text = render_to_string('dashboard/terraform_template', {
                'name' : name,
                'db_name' : db_name,
                'db_password' : db_password,
                'db_user' : db_user,
                'db_instance_name' : name,
                })
            
            # Terraform
            terraform_binary = "/usr/local/bin/terraform"
            terraform_dir = "/opt/terraform/"
            terraform_file = "/opt/terraform/main.tf"
            maintf = open(terraform_file, "a")
            maintf.write(rendered_text)
            maintf.close()
            import os
            os.chdir(terraform_dir)
            import subprocess
            subprocess.run([terraform_binary, "plan"])
            subprocess.run([terraform_binary, "apply", "-auto-approve"])
            cmd_dns = terraform_binary + f' state show aws_instance.{name} | grep public_dns | sed "s/ //g" | cut -d"=" -f2 | sed "s/^.//g" | sed "s/.$//g"'
            cmd_ip = terraform_binary + f' state show aws_instance.{name} | grep public_ip | sed 1d | sed "s/ //g" | cut -d"=" -f2 | sed "s/^.//g" | sed "s/.$//g"'
            cmd_db_ip = terraform_binary + f' state show aws_db_instance.{name} | grep endpoint | sed "s/ //g" | cut -d"=" -f2 | sed "s/^.//g" | sed "s/.$//g" | cut -d":" -f1'

            terraform_public_dns = subprocess.check_output(cmd_dns,shell=True)
            terraform_public_dns = str(terraform_public_dns)[2:-3]
            terraform_public_ip = subprocess.check_output(cmd_ip,shell=True)
            terraform_public_ip = str(terraform_public_ip)[2:-3]
            terraform_db_ip = subprocess.check_output(cmd_db_ip,shell=True)
            terraform_db_ip = str(terraform_db_ip)[2:-3]
            
            # Para instalar Ansible para autoinstalación
            text_ansible_hosts='ubuntu@'+terraform_public_dns+' ansible_ssh_private_key_file=/opt/ansible/key'
            fichero = open('/etc/ansible/hosts','w')
            fichero.write(text_ansible_hosts)
            fichero.close()
            
            # Se cargan las variables en group_vars/all
            db_new_password = generate_random_password()
            db_new_user = db_user + "_new"
            rendered_text = render_to_string('dashboard/all', {
                'domain' : terraform_public_dns,
                'db_ip' : terraform_db_ip,
                'mysql_db' : db_name,
                'mysql_user' : db_user,
                'mysql_password' : db_password,
                'mysql_new_user' : db_new_user,
                'mysql_new_password' : db_new_password,
                'site_name' : web_name,
                'admin_user' : admin_user,
                'admin_password' : admin_password,
                'name_user' : 'admin',
                'surname_user' : 'administrator',
                'server' : name,
                'cms' : cms_type.lower()
                })
            fichero = open('/opt/ansible/group_vars/all','w')
            fichero.write(rendered_text)
            fichero.close()
            
            #Ejecutamos playbook de Ansible para instalar el cms correspondiente
            subprocess.run(["/usr/bin/ansible-playbook", "/opt/ansible/autoinstall.yml"]) # Instalará los ansible_playbooks y además los ejecutará pasandole las variables

            new_server = Servidor.objects.create(
                id=name.replace("_","."),
                name=terraform_public_dns,
                cms_type=cms_type, 
                server_type=server_type, 
                public_ip=terraform_public_ip,
                user_admin_id=Admin, 
                )
            
            return redirect("index")
        else:
            return render(request, 'dashboard/add_new_server.html', {'form' : form})
    elif request.method == 'GET':
        form = formulario_añadir_nuevo_servidor()
    return render(request, 'dashboard/add_new_server.html', {'form' : form})
