from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('delete-item/<int:id>/', views.delete_item, name='delete-item'),
    path('logout/', views.logout, name='logout'),
    path('add/', views.add_new_server, name='add_new_server'),
    # path('not_found/', views.not_found, name='not found')
]