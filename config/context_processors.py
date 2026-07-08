from django.conf import settings

def enable_reportes(request):
    return {'ENABLE_REPORTES': getattr(settings, 'ENABLE_REPORTES', False)}
