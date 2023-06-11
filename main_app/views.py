from django.shortcuts import render, redirect
from .models import Project, Task, Journal, Video
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from dotenv import load_dotenv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from googleapiclient.discovery import build
import os
from decouple import config
from django.views.generic import ListView, DetailView
import googleapiclient.errors
from rest_framework.views import APIView
from rest_framework.response import Response
from oauth2_provider.decorators import protected_resource
from oauth2_provider.views.generic import ProtectedResourceView
from django.http import HttpResponse
import random
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
# from .models import UrlSave


# Create your views here.

def random_class(pick):
    choices = ["table-primary", "table-secondary", "table-success", "table-danger", "table-warning", "table-info", "table-active"]
    pick = random.choice(choices)
    
    random_class(pick)

def index(request):
    projects = Project.objects.filter(user=request.user)
    return render(request, 'index.html', {'projects': projects})

def about(request):
    return render(request, 'about.html')

@login_required
def projects_detail(request, project_id):
    project = Project.objects.get(id=project_id)
    # tasks = Task.objects.filter(id=project_id)
    id_list = Task.project.all().values_list('id')
    tasks_project_doesnt_have = Project.objects.exclude(id__in=id_list)
    
    
    return render(request, 'projects/detail.html', {
        'project':project,
        "tasks": tasks_project_doesnt_have,
        
        })
    
@login_required
def tasks_index(request):
    tasks =  Task.objects.all()
    return render(request, 'tasks_index.html', {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id)
    id_list = task.entries.all().values_list('id') 
    entries_task_doesnt_have = Journal.objects.exclude(id__in=id_list)
    return render(request, 'tasks/task_detail.html', {'task':task})


LoginRequiredMixin, 
def signup(request):
    # POST request
    error_message = ''
        # user is signing up with a form submission
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'invalid signup - try again'
    # GET request
        # user is navigating to signup page to fill out form
    form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'error': error_message
    })

# def assoc_task(request, project_id, task_id):
#     Project.objects.filter(id=project_id).tasks.add(task_id)
#     return redirect('task_list', project_id=project_id)

# def unassoc_task(request, project_id, task_id):
#     Project.objects.filter(id=project_id).tasks.remove(task_id)
#     return redirect('detail', project_id=project_id)
    
class ProjectCreate (LoginRequiredMixin, CreateView):
    model = Project
    fields = ['name', 'technology', 'description', 'github']
    # success_url = '/cats/' # not the preferred way 
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = "__all__"    
    
class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = '/projects/'
class TaskCreate (LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'date', 'completed']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = "__all__"  
    
class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = '/tasks/'
    
class TaskList(LoginRequiredMixin, ListView):
    model = Task


    
    
API_KEY = config('API_KEY')

def search_results(request):
    searched = request.GET.get('searched', '')  
    if searched:
        # Perform the search
        key = config('API_KEY')
        youtube = build('youtube', 'v3', developerKey=key)
        request = youtube.search().list(
            part="snippet",
            maxResults=5,
            q=searched,
            order="date",
            type='video'
        )

        results = request.execute()

        print(results)
        return render(request, 'search/results.html', {'results': results})
    else:
        return render(request, 'search/results.html', {'results': {}})
    
    # def display(request, id):
    #     print(request.META['HTTP_REFERER'])
    # try:
    #     short_url = UrlSave.objects.get(pk=id)
    #     visit_time = short_url.times_visited
    #     short_url.times_visited = short_url.times_visited+1
    #     url = short_url.to_view
    #     short_url.save()
    #     context = {'visit':visit_time,'url':url}
    #     return render(request,'shorturl/previsit.html',context)
    # except:
    #     return HttpResponse('Wrong Url')

