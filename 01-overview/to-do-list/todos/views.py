from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo

# Create your views here.

def todo_list(request):
    """Display all todos"""
    todos = Todo.objects.all()
    return render(request, 'todos/todo_list.html', {'todos': todos})

def todo_create(request):
    """Create a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        Todo.objects.create(title=title, description=description)
        return redirect('todo_list')
    return render(request, 'todos/todo_form.html', {'form_type': 'Create'})

def todo_update(request, pk):
    """Update an existing todo"""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.title = request.POST.get('title')
        todo.description = request.POST.get('description', '')
        todo.completed = 'completed' in request.POST
        todo.save()
        return redirect('todo_list')
    return render(request, 'todos/todo_form.html', {'todo': todo, 'form_type': 'Update'})

def todo_delete(request, pk):
    """Delete a todo"""
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == 'POST':
        todo.delete()
        return redirect('todo_list')
    return render(request, 'todos/todo_confirm_delete.html', {'todo': todo})

def todo_toggle(request, pk):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, pk=pk)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')
