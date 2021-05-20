from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.views.generic.edit import UpdateView,DeleteView

class TaskListView(ListView):
    model = Task
    template_name='todoapp/home.html'
    context_object_name = 'tasks'

class TaskDetaiView(DetailView):
    model = Task
    template_name = 'todoapp/details.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    template_name = 'todoapp/cupdate.html'
    model = Task
    context_object_name = 'task'
    fields = ('name','priority','date')

    def get_success_url(self):
        return reverse_lazy('todoapp:cbvdetails',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'todoapp/delete.html'
    success_url = reverse_lazy('todoapp:cbvhome')

def home(request):
    tasks = Task.objects.all()
    if request.method=='POST':
        name = request.POST['name']
        date = request.POST['date']
        priority = request.POST['priority']
        task = Task(name=name,priority=priority,date=date)
        task.save()
        return redirect('/')
    return render(request,'todoapp/home.html',{'tasks':tasks})
def delete(request,id):
    task = Task.objects.get(id=id)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,'todoapp/delete.html',{'task':task})
def update(request,id):
    task = Task.objects.get(id=id)
    form=TaskForm(instance=task)
    if request.method=='POST':
        form = TaskForm(request.POST or None,instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request,'todoapp/update.html',{'form':form})