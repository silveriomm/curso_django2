from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.contrib import messages
import datetime


@login_required
def taskList(request):
    search = request.GET.get('search')
    filter = request.GET.get('filter')
    tasksDoneRecently = Task.objects.filter(done='done', update_at__gt=datetime.datetime.now()-datetime.timedelta(days=30), user=request.user).count()
    tasksDone = Task.objects.filter(done='done', user=request.user).count()
    tasksDoing = Task.objects.filter(done='doing', user=request.user).count()
    if search:
        tasks_list = Task.objects.filter(title__icontains=search, user=request.user)
        paginator = Paginator(tasks_list, 4)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    elif filter:
        tasks_list = Task.objects.filter(done=filter, user=request.user)
        paginator = Paginator(tasks_list, 4)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
    else:
        tasks_list = Task.objects.all().order_by('-create_at').filter(user=request.user)
        paginator = Paginator(tasks_list, 4)
        page = request.GET.get('page')
        tasks = paginator.get_page(page)
        
    return render(request, 'tasks/list.html',{'tasks':tasks, 'tasksDoneRecently': tasksDoneRecently, 'tasksDone':tasksDone, 'tasksDoing':tasksDoing})

@login_required
def newTask(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.done = 'doing'
            task.user = request.user
            task.save()
            messages.info(request, 'Tarefa adicionada com sucesso!')
            return redirect('/')
    else:
        form = TaskForm()
        return render(request, 'tasks/addtask.html', {'form':form})

@login_required
def editTask(request, id):
    task = get_object_or_404(Task, pk=id)
    form = TaskForm(instance=task)
    if(request.method == 'POST'):
        form = TaskForm(request.POST, instance=task)
        if(form.is_valid()):
            task.save()
            messages.info(request, 'Tarefa alterada com sucesso!')
            return redirect('/')
        else:
            return render(request, 'tasks/edittask.html',{'form':form, 'task':task})    
    else:
        return render(request, 'tasks/edittask.html',{'form':form, 'task':task})


@login_required
def deleteTask(request, id):
    task = get_object_or_404(Task, pk=id)
    task.delete()
    messages.info(request, 'Tarefa excluída com sucesso!')
    return redirect('/')


@login_required
def changeStatus(request, id):
    task = get_object_or_404(Task, pk=id)
    if(task.done == 'doing'):
        task.done = 'done'
    else:
        task.done = 'doing'

    task.save()
    return redirect('/')



def taskView(request, id):
    task = get_object_or_404(Task, pk=id)
    return render(request, 'tasks/task.html', {'task':task})

def about(request):
    return render(request, 'tasks/about.html')
