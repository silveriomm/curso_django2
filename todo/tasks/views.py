from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from .models import Task

def taskList(request):
    tasks = Task.objects.all().order_by('-create_at')
    return render(request, 'tasks/list.html',{'tasks':tasks})

def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form':form})


def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)
    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if(form.is_valid()):
            task.save()
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html',{'form':form, 'task':task})    
    else:
        return render(request, 'tasks/edittask.html',{'form':form, 'task':task})


def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task':task})

