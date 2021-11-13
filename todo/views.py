from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.shortcuts import redirect


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')



def signup_user(request):
    if request.method == 'GET':
        return render(request, 'todo/signup_user.html', {'form':UserCreationForm()})
    if request.POST['password1'] != request.POST['password2']:
        return render(request, 'todo/signup_user.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})
        
    try:
        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('current_todos')
    except IntegrityError:
        return render(request, 'todo/signup_user.html', {'form':UserCreationForm(), 'error':'User already exists'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'todo/login_user.html', {'form':AuthenticationForm()})
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return render(request, 'todo/login_user.html', {'form':AuthenticationForm(), 'error': 'Username password did not match.'})
    
    login(request, user)
    return redirect('current_todos')



def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html')
    else:
        pass

def current_todos(request):
    return(render(request, 'todo/current_todos.html'))

