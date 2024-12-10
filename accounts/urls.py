# В accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('nomenclature/', views.nomenclature_list, name='nomenclature_list'),
    path('lsi/', views.lsi_list, name='lsi_list'),
    path('nomenclature/create/', views.create_nomenclature, name='create_nomenclature'),
    path('lsi/create/', views.create_lsi, name='create_lsi'),
    path('nomenclature/edit/<int:pk>/', views.edit_nomenclature, name='edit_nomenclature'),
    path('lsi/edit/<int:pk>/', views.edit_lsi, name='edit_lsi'),
    path('nomenclature/delete/<int:pk>/', views.delete_nomenclature, name='delete_nomenclature'),
    path('lsi/delete/<int:pk>/', views.delete_lsi, name='delete_lsi'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('export/excel/', views.export_to_excel, name='export_to_excel'),
    path('export/xml/', views.export_to_xml, name='export_to_xml'),
    path('import/excel/', views.import_from_excel, name='import_from_excel'),
    path('import/xml/', views.import_from_xml, name='import_from_xml'),
]

