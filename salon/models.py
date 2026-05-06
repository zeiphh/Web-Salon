from django.db import models
from django.contrib.auth.models import User


class Servicio(models.Model):
    CATEGORIAS = [
        ('renta',           'Renta del salón'),
        ('decoracion',      'Decoración'),
        ('sonido',          'Música y sonido'),
        ('entretenimiento', 'Entretenimiento'),
        ('otro',            'Otro'),
    ]
    nombre      = models.CharField(max_length=60)
    descripcion = models.TextField(max_length=250)
    precio      = models.DecimalField(max_digits=8, decimal_places=2)
    categoria   = models.CharField(max_length=20, choices=CATEGORIAS, default='otro')
    activo      = models.BooleanField(default=True)
    creado_en   = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'{self.nombre} — ${self.precio}'


class PerfilUsuario(models.Model):
    ROLES = [
        ('admin',    'Administrador'),
        ('empleado', 'Empleado'),
        ('cliente',  'Cliente'),
    ]
    usuario  = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol      = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f'{self.usuario.username} ({self.get_rol_display()})'

    @property
    def es_admin(self):
        return self.rol == 'admin'

    @property
    def es_empleado(self):
        return self.rol in ('admin', 'empleado')
