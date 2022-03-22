from django.shortcuts import render, redirect
from dashboard.models import Usuario

# Create your views here.
from django.http import HttpResponse, HttpResponseForbidden

app_name='login'

# def index(request):
#     return HttpResponse(f"Hello, world. You're at the {app_name} index.")

# def index(request):
#     if 'user' in request.session:
#         current_user = request.session['user']
#         return render(request, 'login/index.html', {
#         'current_user' : current_user
#     })
#     else:
#         return redirect('login')
#     return render(request, 'index.html')

def login(request):
    if request.method == 'POST' :
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')## asegurar inyecciones sql
        
        check_user = Usuario.objects.filter(email=user_email, password=user_password).get()
        
        if check_user :
            request.session['user'] = check_user.username
            return redirect('/dashboard')
        else:
            return HttpResponseForbidden()

    return render(request, 'login/index.html',{
        
    })

