from django.urls import path
from . import views

urlpatterns = [
    # Públicas
    path('',           views.index,         name='index'),
    path('nosotros/',  views.nosotros,       name='nosotros'),
    path('servicios/', views.servicios_page, name='servicios'),
    path('galeria/',   views.galeria,        name='galeria'),
    path('contacto/',  views.contacto,       name='contacto'),

    # CRUD Servicios
    path('panel/servicios/',                    views.lista_servicios_admin, name='lista_servicios_admin'),
    path('panel/servicios/alta/',               views.alta,                  name='alta'),
    path('panel/servicios/<int:pk>/editar/',    views.modificar,             name='modificar'),
    path('panel/servicios/<int:pk>/eliminar/',  views.eliminar,              name='eliminar'),

    # CRUD Usuarios
    path('panel/usuarios/',                     views.lista_usuarios,    name='lista_usuarios'),
    path('panel/usuarios/nuevo/',               views.registro_usuario,  name='registro_usuario'),
    path('panel/usuarios/<int:pk>/editar/',     views.modificar_usuario, name='modificar_usuario'),
    path('panel/usuarios/<int:pk>/eliminar/',   views.eliminar_usuario,  name='eliminar_usuario'),

    # Registro público
    path('registro/', views.registro_cliente, name='registro_cliente'),

    # AJAX
    path('ajax/verificar-nombre/',   views.ajax_verificar_nombre,  name='ajax_verificar_nombre'),
    path('ajax/verificar-usuario/',  views.ajax_verificar_usuario, name='ajax_verificar_usuario'),
]
