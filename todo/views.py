from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


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


@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def create_todo(request):
    if request.method == 'GET':
        return render(request, 'todo/create_todo.html', {'form': TodoForm})
    try:
        form = TodoForm(request.POST)
        new_todo = form.save(commit=False)
        new_todo.user = request.user
        new_todo.save()
        return redirect('current_todos')
    except ValueError:
        return render(request, 'todo/create_todo.html', {'form': TodoForm, 'error': 'Bad data passed in. Try Again'})

@login_required
def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
    return render(request, 'todo/current_todos.html', {'todos':todos})

@login_required
def completed_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completed__isnull=False).order_by('-date_completed')
    return render(request, 'todo/completed_todos.html', {'todos':todos})

@login_required
def view_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/view_todo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('current_todos')
        except ValueError:
            return render(request, 'todo/view_todo.html', {'todo':todo, 'form':form, 'error': 'Bad data passed in. Try Again'}) 

@login_required
def complete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_completed = timezone.now()
        todo.save()
        return redirect('current_todos')

@login_required
def delete_todo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('current_todos')