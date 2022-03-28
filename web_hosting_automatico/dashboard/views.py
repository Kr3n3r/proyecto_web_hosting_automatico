from multiprocessing import context
from django.shortcuts import redirect, render
import django.contrib.auth

# Create your views here.
from django.http import HttpResponse
from django.template import loader
from .models import Servidor, Usuario

app_name='dashboard'

# def index(request):
#     return HttpResponse(f"Hello, world. You're at the {app_name} index.")

def index(request):
    # username = recibido por POST o por -->session<--
    try:
        username = request.session['user']
    except:
        return redirect('login')
    server_list = Servidor.objects.filter(user_admin=username)
    return render(request, 'dashboard/index.html', {
        'user_name' : request.session['user'],
        'server_list' : server_list,
    })

def delete_item(request,id):
    server = Servidor.objects.get(id=id)
    if server.user_admin_id == request.session['user'] :
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
        ## así se hace, cambiar
    except:
        return redirect('login')
    return redirect('login')

# def not_found(request):
#     context = {
        
#     }
#     return render(request, 'dashboard/404.html', context)

def add_new_server(request):
    try:
        username = request.session['user']
    except:
        redirect('login')
    context = {
        'cms_type' : Servidor.CMS,
        'server_type' : Servidor.SERVER_TYPES,
        
    }
    return render(request, 'dashboard/add_new_server.html', context)

from .forms import formulario_añadir_nuevo_servidor
from django.forms.utils import ErrorList
class div_invalidfeedback(ErrorList):  
    def __str__(self):
            return self.as_divs()
    def as_divs(self):
            if self: 
                return '<div class="invalid-feedback">%s</div>' % ''.join(['%s' % e for e in self])
            return ''

def añadir_nuevo_servidor(request):
    if request.method == 'POST' :
        form = formulario_añadir_nuevo_servidor(data=request.POST, error_class=div_invalidfeedback)
        form = form.name_is_valid()
        if form.is_valid():
            return render(request, 'dashboard/index.html', {})
        else:
            return render(request, 'dashboard/add_new_server.html', {'form' : form})
    elif request.method == 'GET':
        form = formulario_añadir_nuevo_servidor()
    return render(request, 'dashboard/add_new_server.html', {'form' : form})