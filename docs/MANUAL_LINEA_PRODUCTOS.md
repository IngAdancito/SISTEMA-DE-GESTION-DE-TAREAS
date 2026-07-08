# LÍNEA DE PRODUCTOS BASADA EN DJANGO
## Sistema de Gestión de Tareas - Manual de Producto

---

## 1. INTRODUCCIÓN

Este documento describe la Línea de Productos de Software (SPL) implementada sobre
el Sistema de Gestión de Tareas desarrollado en Django. Se presentan las variantes,
la configuración de características y las instrucciones para activar/desactivar
funcionalidades.

---

## 2. ARQUITECTURA DE LA LÍNEA DE PRODUCTOS

### 2.1 Patrimonio Común (Core Assets)

Todas las variantes comparten:

| Componente | Descripción | Tipo |
|---|---|---|
| `tasks/` | App CRUD de tareas (modelo, vistas, URLs, templates) | **Core** obligatorio |
| `accounts/` | Autenticación (registro, login, logout) | **Reutilizable** |
| `templates/base.html` | Template base con navbar, alerts, footer | **Reutilizable** |
| `static/style.css` | Hojas de estilo base | **Reutilizable** |
| `config/` | Settings, URLs raíz, WSGI/ASGI | **Infraestructura** |

### 2.2 Variabilidad (Features Opcionales)

| Feature | Variante A | Variante B | App asociada |
|---|---|---|---|
| Exportar CSV | Desactivado | Activado | `reportes/` |
| Notificaciones | Desactivado | Activado (futuro) | — |
| Panel Admin Django | Activado | Activado | `django.contrib.admin` |

### 2.3 Patrón de Reutilización

Se utilizó el patrón **Feature Toggle** (también conocido como bandera de
funcionalidad). Las características opcionales se aíslan en apps Django
independientes y se activan/desactivan mediante banderas de configuración
en `settings.py`, sin modificar el código base.

---

## 3. INSTRUCCIONES DE CONFIGURACIÓN

### 3.1 Seleccionar Variante

Editar el archivo `.env` en la raíz del proyecto:

```ini
# Variante A - Básica (sin funcionalidades extra)
PRODUCT_VARIANT=A

# Variante B - Completa (con exportación CSV y más)
PRODUCT_VARIANT=B
```

### 3.2 Archivo de Configuración de Variantes

`config/config_product.py`:

```python
PRODUCT_A = {
    'ENABLE_REPORTES': False,
    'ENABLE_NOTIFICATIONS': False,
    'PRODUCT_NAME': 'Sistema de Gestión de Tareas - Variante A (Básica)',
}

PRODUCT_B = {
    'ENABLE_REPORTES': True,
    'ENABLE_NOTIFICATIONS': True,
    'PRODUCT_NAME': 'Sistema de Gestión de Tareas - Variante B (Completa)',
}
```

### 3.3 Mecanismo de Activación

En `config/settings.py`:

```python
from config.config_product import PRODUCT_A, PRODUCT_B

PRODUCT_VARIANT = config('PRODUCT_VARIANT', default='A')

if PRODUCT_VARIANT == 'B':
    PRODUCT_CONFIG = PRODUCT_B
else:
    PRODUCT_CONFIG = PRODUCT_A

ENABLE_REPORTES = PRODUCT_CONFIG['ENABLE_REPORTES']
if ENABLE_REPORTES:
    INSTALLED_APPS += ['reportes']
```

En `config/urls.py`:

```python
if settings.ENABLE_REPORTES:
    urlpatterns += [
        path('reportes/', include('reportes.urls')),
    ]
```

En templates (`base.html`):

```html
{% if ENABLE_REPORTES %}
    <a href="{% url 'export_tasks' %}">Exportar CSV</a>
{% endif %}
```

---

## 4. RECOMENDACIONES PARA REUTILIZAR APPS DJANGO

1. **Aislar funcionalidades en apps independientes** — Cada funcionalidad
   opcional debe ser una app Django separada con sus propios modelos, vistas,
   URLs y templates.

2. **Usar banderas de configuración** — Controlar la inclusión de apps,
   registro de rutas y visibilidad en templates mediante variables en
   `settings.py`.

3. **Mantener un core mínimo** — La app principal debe funcionar sin las
   apps opcionales. No debe haber dependencias forzosas.

4. **Usar context processors** — Para pasar banderas de configuración a
   todos los templates sin repetir código.

5. **Documentar cada feature toggle** — Indicar qué hace, cómo se activa
   y qué dependencias tiene.

---

## 5. DIAGRAMA DE VARIABILIDAD (SPL)

```
                    ┌─────────────────────────────┐
                    │   SISTEMA DE GESTIÓN         │
                    │      DE TAREAS               │
                    └─────────────┬───────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
    ┌───────┴───────┐     ┌───────┴───────┐     ┌───────┴───────┐
    │   tasks/      │     │  accounts/    │     │  reportes/    │
    │   (Core)      │     │ (Reutilizable)│     │  (Opcional)   │
    │   Obligatorio │     │  Obligatorio  │     │               │
    └───────────────┘     └───────────────┘     └───────────────┘
                                                       │
                                              ┌────────┴────────┐
                                              │                 │
                                       ACTIVADO           DESACTIVADO
                                      (Variante B)       (Variante A)
```

---

## 6. TABLA DE VARIANTES Y CONFIGURACIÓN

| Característica | Variante A (Básica) | Variante B (Completa) |
|---|---|---|
| **PRODUCT_VARIANT** | A | B |
| **PRODUCT_NAME** | Sistema de Gestión de Tareas - Variante A (Básica) | Sistema de Gestión de Tareas - Variante B (Completa) |
| **ENABLE_REPORTES** | False | True |
| **ENABLE_NOTIFICATIONS** | False | True |
| **Exportar CSV** | No disponible | Disponible |
| **Tasks CRUD** | Sí | Sí |
| **Autenticación** | Sí | Sí |
| **Panel Admin** | Sí | Sí |

---

## 7. CAPTURAS DE PANTALLA

### 7.1 Variante A (Básica)
*[Insertar aquí captura de pantalla mostrando el sistema sin el botón "Exportar CSV"]*

### 7.2 Variante B (Completa)
*[Insertar aquí captura de pantalla mostrando el sistema con el botón "Exportar CSV" visible en el navbar]*

---

## 8. CONCLUSIÓN

La línea de productos implementada permite generar dos variantes del sistema
a partir de una misma base de código, utilizando el patrón Feature Toggle.
La variante A ofrece funcionalidad básica de gestión de tareas, mientras que
la variante B agrega exportación CSV y prepara el terreno para notificaciones.
Este enfoque facilita el mantenimiento, la reutilización y la escalabilidad
del producto.
