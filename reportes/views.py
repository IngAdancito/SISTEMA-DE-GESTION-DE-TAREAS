import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from tasks.models import Task

@login_required
def export_tasks_csv(request):
    tasks = Task.objects.filter(created_by=request.user)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tareas.csv"'
    writer = csv.writer(response)
    writer.writerow(['Titulo', 'Descripcion', 'Estado', 'Prioridad', 'Fecha Limite', 'Creada'])
    for t in tasks:
        writer.writerow([t.title, t.description, t.status, t.priority, t.due_date, t.created_at])
    return response
