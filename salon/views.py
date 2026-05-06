from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import Servicio, PerfilUsuario
from .forms import ServicioForm, RegistroUsuarioForm, ModificarUsuarioForm, RegistroClienteForm


# ── Helpers de rol ────────────────────────────────────────────
def es_admin(user):
    return hasattr(user, 'perfil') and user.perfil.es_admin

def es_empleado_o_admin(user):
    return hasattr(user, 'perfil') and user.perfil.es_empleado


# ── Páginas públicas ──────────────────────────────────────────
def index(request):
    # Sesión: contador de visitas (Paso 3)
    request.session['visitas'] = request.session.get('visitas', 0) + 1
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'salon/index.html', {
        'servicios': servicios,
        'visitas':   request.session['visitas'],
    })

def nosotros(request):
    return render(request, 'salon/nosotros.html')

def servicios_page(request):
    servicios = Servicio.objects.filter(activo=True)
    return render(request, 'salon/servicios.html', {'servicios': servicios})

def galeria(request):
    return render(request, 'salon/galeria.html')

def contacto(request):
    return render(request, 'salon/contacto.html')


# ── CRUD Servicios ────────────────────────────────────────────
@login_required
def lista_servicios_admin(request):
    if not es_empleado_o_admin(request.user):
        return redirect('index')
    servicios = Servicio.objects.all().order_by('id')
    return render(request, 'salon/lista_servicios.html', {'servicios': servicios})


@login_required
def alta(request):
    if not es_empleado_o_admin(request.user):
        messages.error(request, 'No tienes permiso para esta acción.')
        return redirect('index')
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio registrado correctamente.')
            return redirect('lista_servicios_admin')
    else:
        form = ServicioForm()
    return render(request, 'salon/alta.html', {'form': form})


@login_required
def modificar(request, pk):
    if not es_empleado_o_admin(request.user):
        messages.error(request, 'No tienes permiso para esta acción.')
        return redirect('index')
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Servicio actualizado correctamente.')
            return redirect('lista_servicios_admin')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'salon/modificar.html', {'form': form, 'servicio': servicio})


@login_required
def eliminar(request, pk):
    if not es_admin(request.user):
        messages.error(request, 'Solo los administradores pueden eliminar servicios.')
        return redirect('index')
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        nombre = servicio.nombre
        servicio.delete()
        messages.success(request, f'Servicio "{nombre}" eliminado.')
        return redirect('lista_servicios_admin')
    return render(request, 'salon/eliminar.html', {'servicio': servicio})


# ── CRUD Usuarios ─────────────────────────────────────────────
@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = User.objects.select_related('perfil').all().order_by('id')
    return render(request, 'salon/lista_usuarios.html', {'usuarios': usuarios})


@login_required
@user_passes_test(es_admin)
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario registrado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'salon/registro_usuario.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def modificar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = ModificarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('lista_usuarios')
    else:
        form = ModificarUsuarioForm(instance=usuario)
    return render(request, 'salon/modificar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado.')
        return redirect('lista_usuarios')
    return render(request, 'salon/eliminar_usuario.html', {'usuario': usuario})


# ── Registro público (clientes) ──────────────────────────────
def registro_cliente(request):
    """Cualquier visitante puede crear su cuenta con rol cliente."""
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(
                usuario  = user,
                rol      = 'cliente',
                telefono = form.cleaned_data.get('telefono', ''),
            )
            messages.success(request, '¡Cuenta creada correctamente! Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroClienteForm()
    return render(request, 'salon/registro_cliente.html', {'form': form})
@require_GET
def ajax_verificar_nombre(request):
    """Verifica en tiempo real si un nombre de servicio ya existe en la BD."""
    nombre  = request.GET.get('nombre', '').strip()
    excluir = request.GET.get('excluir_id')
    if not nombre:
        return JsonResponse({'disponible': True})
    qs = Servicio.objects.filter(nombre__iexact=nombre)
    if excluir:
        qs = qs.exclude(pk=excluir)
    return JsonResponse({'disponible': not qs.exists()})


@require_GET
def ajax_verificar_usuario(request):
    """Verifica en tiempo real si un nombre de usuario ya existe en la BD."""
    username = request.GET.get('username', '').strip()
    excluir  = request.GET.get('excluir_id')
    if not username:
        return JsonResponse({'disponible': True})
    qs = User.objects.filter(username__iexact=username)
    if excluir:
        qs = qs.exclude(pk=excluir)
    return JsonResponse({'disponible': not qs.exists()})
