# Salón La Haciendita — Django + PostgreSQL
## Práctica Unidad 4

---

## PASO 0 — PostgreSQL (en pgAdmin o psql)

```sql
CREATE DATABASE haciendita_db;
CREATE USER haciendita_user WITH PASSWORD 'haciendita2026';
GRANT ALL PRIVILEGES ON DATABASE haciendita_db TO haciendita_user;
\c haciendita_db
GRANT ALL ON SCHEMA public TO haciendita_user;
```

---

## PASO 1 — Instalar dependencias

```bash
cd haciendita_django
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

---

## PASO 2 — Crear tablas en PostgreSQL

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## PASO 3 — Crear superusuario

```bash
python manage.py createsuperuser
```

Luego asignarle perfil admin desde la shell:
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
from salon.models import PerfilUsuario
u = User.objects.get(username='nothi')
PerfilUsuario.objects.create(usuario=u, rol='admin')
exit()
```

---

## PASO 4 — Levantar servidor

```bash
python manage.py runserver
```
Abrir: http://127.0.0.1:8000

---

## PASO 5 — HTTPS (Paso 4 de la práctica)

Agregar 'sslserver' a INSTALLED_APPS en settings.py, luego:
```bash
python manage.py runsslserver 0.0.0.0:8443
```
Abrir: https://127.0.0.1:8443

---

## URLs del sistema

| URL | Descripción | Acceso |
|-----|-------------|--------|
| / | Inicio | Público |
| /nosotros/ | Sobre nosotros | Público |
| /servicios/ | Servicios | Público |
| /galeria/ | Galería | Público |
| /contacto/ | Contacto | Público |
| /login/ | Iniciar sesión | Público |
| /panel/servicios/ | Lista servicios | Empleado/Admin |
| /panel/servicios/alta/ | Alta servicio | Empleado/Admin |
| /panel/servicios/N/editar/ | Modificar servicio | Empleado/Admin |
| /panel/servicios/N/eliminar/ | Eliminar servicio | Solo Admin |
| /panel/usuarios/ | Lista usuarios | Solo Admin |
| /panel/usuarios/nuevo/ | Registrar usuario | Solo Admin |
| /admin/ | Panel Django admin | Superusuario |
| /ajax/verificar-nombre/ | AJAX nombre servicio | Interno |
| /ajax/verificar-usuario/ | AJAX username | Interno |
