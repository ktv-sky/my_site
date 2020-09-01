from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from .models import Task
from .forms import TaskForm


@login_required
def tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by('-date_added')
    return render(request, 'tasks/tasks.html', {
        'tasks': tasks
    })

@login_required
def new_task(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(data=request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.owner = request.user
            new_task.save()
            return redirect('tasks:tasks')

    return render(request, 'tasks/new_task.html', {
        'form': form
    })
