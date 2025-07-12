from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TaskForm, ConfirmPasswordForm, ProfileImageForm
from .models import Task

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'tasks/login.html', {'error': 'Invalid credentials'})
    return render(request, 'tasks/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def delete_all_tasks(request):
    if request.method == "POST":
        request.user.task_set.all().delete()
        return redirect('task_list')
    return render(request, 'tasks/delete_all_confirm.html')

@login_required
def delete_account(request):
    if request.method == "POST":
        form = ConfirmPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('login')
    else:
        form = ConfirmPasswordForm(request.user)
    return render(request, 'tasks/delete_account.html', {'form': form})

@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = ProfileImageForm(instance=request.user.profile)
    return render(request, 'tasks/update_profile_picture.html', {'form': form})