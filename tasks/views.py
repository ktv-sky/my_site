from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Task


@login_required
def tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })
