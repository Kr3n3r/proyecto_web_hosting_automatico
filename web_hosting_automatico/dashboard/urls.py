from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete-item/<str:id>/', views.delete_item, name='delete-item'),
    path('logout/', views.logout, name='logout'),
    path('add/', views.añadir_nuevo_servidor, name='add_new_server'),
]