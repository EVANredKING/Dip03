# accounts/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('nomenclature/create/', views.nomenclature_create, name='nomenclature_create'),
    path('nomenclature/update/<int:pk>/', views.nomenclature_update, name='nomenclature_update'),
    path('nomenclature/delete/<int:pk>/', views.nomenclature_delete, name='nomenclature_delete'),
    path('lsi/create/', views.lsi_create, name='lsi_create'),
    path('lsi/update/<int:pk>/', views.lsi_update, name='lsi_update'),
    path('lsi/delete/<int:pk>/', views.lsi_delete, name='lsi_delete'),
]
