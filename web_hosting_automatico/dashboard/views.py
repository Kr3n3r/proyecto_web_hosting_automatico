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
        
    }
    return render(request, 'dashboard/add_new_server.html', context)