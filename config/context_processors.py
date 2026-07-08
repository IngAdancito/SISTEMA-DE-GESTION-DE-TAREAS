from django.conf import settings

def enable_reportes(request):
    return {
        'ENABLE_REPORTES': getattr(settings, 'ENABLE_REPORTES', False),
        'PRODUCT_NAME': getattr(settings, 'PRODUCT_CONFIG', {}).get('PRODUCT_NAME', 'Sistema de Gesti\u00f3n de Tareas'),
    }
