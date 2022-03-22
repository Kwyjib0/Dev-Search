import profile
import re
import django
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout # for authentication
from django.contrib.auth.decorators import login_required # to require login to access a page
from django.contrib import messages # for flash messages
from django.contrib.auth.models import User # for authentication
from .forms import ProfileForm, SkillForm, CustomUserCreationForm # customized django UserCreationForm from forms.py
from .models import Profile

# for authentication
def loginUser(request):
    page = 'login'
    # keeps users already logged in from accessing login page
    # if try to go to this page redirected to profiles page
    if request.user.is_authenticated:
        return redirect('profiles')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # make sure username exists in database
        try:    
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')
        # authenticate function takes and username and password and makes sure
        # that pw matches the username and returns either the user instance or none
        # queries the database for user that matches username and password
        user = authenticate(request, username=username, password=password)
        # checks if user exists
        if user is not None:
            # creates a session for the user in the database and add that to browser's
            # cookies so that we know the user is logged in
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request=request, template_name="users/login_register.html")

def logoutUser(request):
    logout(request)
    messages.info(request, 'User was successfully logged out.')
    return redirect('login')

def registerUser(request):
    page = 'register'
    # create an instance of django's user creation form for adding user to db
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # saving form & creating and holding a temporary user instance 
            # in case we want to modify something such as capitalization in username
            # or if need  to add data e.g. field value is null
            user = form.save(commit=False)
            # makes username all lower case, so not case sensitive
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created.')
            # logs new user in when registers
            login(request, user)
            return redirect('edit-account')

        else:
            messages.error(request, 'An error has occurred. Please try again.')
    context = {'page': page, 'form': form}
    return render(request=request, template_name="users/login_register.html", context=context)

def profiles(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request=request, template_name="users/profiles.html", context=context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    # excludes skills that have no description, description = ""
    topSkills = profile.skill_set.exclude(description__exact="")
    # skills w/o a description, excludes those w/ a description
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills};
    return render(request=request, template_name="users/user-profile.html", context=context)

# decarator this requires user to be logged in to access this page
# and redirects to login page if not logged in
@login_required(login_url='login')
def userAccount(request):
    # request.user gets logged in user
    profile = request.user.profile
    # all skills, w/ & w/o a description
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {'profile': profile,'skills': skills, 'projects': projects};
    return render(request=request, template_name="users/account.html", context=context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    # instance = profile prefills fields in edit form
    form = ProfileForm(instance=profile) 
    if request.method == 'POST':
        # need request.FILES for image file
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()            
            return redirect('account')

    context = {'form': form}
    return render(request=request, template_name="users/profile_form.html", context=context)

@login_required(login_url='login')
def createSkill(request):
    # get who will be the owner of the skill being created (whoever is logged in)
    profile = request.user.profile
    # get the form
    form = SkillForm()

    if request.method == 'POST':
        # when process data, pass in post data
        form = SkillForm(request.POST)
        # check if data passed in is valid
        if form.is_valid():
            # gives us the instance of the skill
            skill = form.save(commit=False)
            # set the owner for the newly created skill
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request=request, template_name="users/skill_form.html", context=context)

@login_required(login_url='login')
def updateSkill(request, pk):
    # get who will be the owner of the skill being created (whoever is logged in)
    profile = request.user.profile
    # get the skill to be edited by its id/pk
    skill = profile.skill_set.get(id=pk)
    # set the instance of the skill to be edited prefilling it in the form
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        # when process data, pass in post data and skill instance being edited
        form = SkillForm(request.POST, instance=skill)
        # check if data passed in is valid
        if form.is_valid():
            form.save()            
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')

    context = {'form': form}
    return render(request=request, template_name="users/skill_form.html", context=context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()            
        messages.success(request, 'Skill was deleted successfully!')
        return redirect('account')
    context = {'object': skill}
    return render(request=request, template_name="delete_template.html", context=context)