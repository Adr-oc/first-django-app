from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
import json
from .models import Todo, Category, Note

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'app/landing_page.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Por favor inicia sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('landing_page')

@login_required
def dashboard(request):
    todos = Todo.objects.filter(user=request.user).order_by('todo_order', '-created_at')
    categories = Category.objects.filter(user=request.user)
    status_groups = {
        'todo': todos.filter(status='todo'),
        'in_progress': todos.filter(status='in_progress'),
        'review': todos.filter(status='review'),
        'done': todos.filter(status='done'),
    }
    context = {
        'todos': todos,
        'categories': categories,
        'status_groups': status_groups,
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'app/categories.html', {'categories': categories})

@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#3B82F6')
        if name:
            Category.objects.create(user=request.user, name=name, color=color)
            messages.success(request, 'Categoría creada exitosamente.')
        return redirect('categories')
    return render(request, 'app/add_category.html')

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color')
        if name:
            category.name = name
            category.color = color
            category.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
        return redirect('categories')
    return render(request, 'app/edit_category.html', {'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
    return redirect('categories')

@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        category_id = request.POST.get('category')
        priority = request.POST.get('priority', 'medium')
        due_date_str = request.POST.get('due_date')
        
        if title:
            todo = Todo.objects.create(
                user=request.user,
                title=title,
                description=description,
                priority=priority
            )
            
            if category_id:
                try:
                    category = Category.objects.get(id=category_id, user=request.user)
                    todo.category = category
                except Category.DoesNotExist:
                    pass
            
            if due_date_str:
                try:
                    todo.due_date = timezone.datetime.strptime(due_date_str, '%Y-%m-%d')
                except ValueError:
                    pass
            
            todo.save()
            messages.success(request, 'Tarea creada exitosamente.')
            return redirect('dashboard')
    
    categories = Category.objects.filter(user=request.user)
    return render(request, 'app/add_todo.html', {'categories': categories})

@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'toggle':
            todo.completed = not todo.completed
            todo.save()
            messages.success(request, 'Estado de la tarea actualizado.')
        elif action == 'delete':
            todo.delete()
            messages.success(request, 'Tarea eliminada exitosamente.')
            return redirect('dashboard')
        elif action == 'update':
            title = request.POST.get('title')
            description = request.POST.get('description', '')
            category_id = request.POST.get('category')
            status = request.POST.get('status')
            priority = request.POST.get('priority')
            
            if title:
                todo.title = title
                todo.description = description
                todo.status = status
                todo.priority = priority
                
                if category_id:
                    try:
                        category = Category.objects.get(id=category_id, user=request.user)
                        todo.category = category
                    except Category.DoesNotExist:
                        todo.category = None
                else:
                    todo.category = None
                
                todo.save()
                messages.success(request, 'Tarea actualizada exitosamente.')
    
    categories = Category.objects.filter(user=request.user)
    return render(request, 'app/todo_detail.html', {'todo': todo, 'categories': categories})

@login_required
def add_note(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Note.objects.create(todo=todo, content=content)
            messages.success(request, 'Nota agregada exitosamente.')
    return redirect('todo_detail', todo_id=todo_id)

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, todo__user=request.user)
    todo_id = note.todo.id
    note.delete()
    messages.success(request, 'Nota eliminada exitosamente.')
    return redirect('todo_detail', todo_id=todo_id)

@login_required
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return JsonResponse({'success': True, 'completed': todo.completed})

@csrf_exempt
@require_POST
@login_required
def update_todo_order(request):
    try:
        data = json.loads(request.body)
        todo_id = data.get('todo_id')
        new_status = data.get('status')
        new_order = data.get('order', 0)
        
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.status = new_status
        todo.todo_order = new_order
        todo.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
