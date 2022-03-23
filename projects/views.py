from re import T
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required # to require login to access a page
from .models import Project, Tag
from .forms import ProjectForm
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context= {'projects':projects, 'search_query': search_query, 'custom_range':custom_range}
    return render(request=request, template_name='projects/projects.html', context=context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    context={'project':projectObj}
    return render(request=request, template_name='projects/single-project.html', context=context)

# decarator this requires user to be logged in to access this page
# and redirects to login page if not logged in
@login_required(login_url='login')
def createProject(request):
    # get logged in user to have profile to connect project to
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # gives us the instance of the project
            project = form.save(commit=False)
            # update owner attribute of the project
            project.owner = profile
            project.save()
            return redirect('projects')
    context = {'form': form}
    return render(request=request, template_name='projects/project_form.html', context=context)

# decarator this requires user to be logged in to access this page
# and redirects to login page if not logged in
@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')
    context = {'form': form}
    return render(request=request, template_name='projects/project_form.html', context=context)

# decarator this requires user to be logged in to access this page
# and redirects to login page if not logged in
@login_required(login_url='login')
def deleteProject(request, pk):    
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    context = {'object': project}
    return render(request=request, template_name='delete_template.html', context=context)