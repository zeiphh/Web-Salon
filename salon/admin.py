from django.contrib import admin
from .models import Servicio, PerfilUsuario

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre', 'categoria', 'precio', 'activo')
    list_filter   = ('categoria', 'activo')
    search_fields = ('nombre',)
    list_editable = ('activo',)

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display  = ('usuario', 'rol', 'telefono')
    list_filter   = ('rol',)
