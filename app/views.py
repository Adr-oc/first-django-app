from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import Todo, Category, Note
from .forms import TodoForm, CategoryForm, NoteForm
import json

def landing_page(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'app/landing_page.html')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    """Custom logout view"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('landing_page')

@login_required
def dashboard(request):
    """Dashboard with Kanban board view"""
    todos = Todo.objects.filter(user=request.user).order_by('order', '-created_at')
    categories = Category.objects.filter(user=request.user)
    
    # Group todos by status
    todo_items = todos.filter(status='todo')
    in_progress_items = todos.filter(status='in_progress')
    done_items = todos.filter(status='done')
    
    context = {
        'todo_items': todo_items,
        'in_progress_items': in_progress_items,
        'done_items': done_items,
        'categories': categories,
    }
    return render(request, 'app/dashboard.html', context)

@login_required
def dashboard_content(request):
    """AJAX endpoint for dashboard content"""
    todos = Todo.objects.filter(user=request.user).order_by('order', '-created_at')
    categories = Category.objects.filter(user=request.user)
    
    todo_items = todos.filter(status='todo')
    in_progress_items = todos.filter(status='in_progress')
    done_items = todos.filter(status='done')
    
    context = {
        'todo_items': todo_items,
        'in_progress_items': in_progress_items,
        'done_items': done_items,
        'categories': categories,
    }
    return render(request, 'app/dashboard_content.html', context)

@login_required
def list_view(request):
    """List view of todos"""
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'todos': todos,
        'categories': categories,
    }
    return render(request, 'app/list_view.html', context)

@login_required
def list_view_content(request):
    """AJAX endpoint for list view content"""
    todos = Todo.objects.filter(user=request.user).order_by('-created_at')
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'todos': todos,
        'categories': categories,
    }
    return render(request, 'app/list_view_content.html', context)

@login_required
def todo_detail(request, todo_id):
    """Detail view for a specific todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    notes = todo.notes.all()
    
    if request.method == 'POST':
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.todo = todo
            note.save()
            messages.success(request, 'Nota agregada exitosamente.')
            return redirect('todo_detail', todo_id=todo.id)
    else:
        note_form = NoteForm()
    
    context = {
        'todo': todo,
        'notes': notes,
        'note_form': note_form,
    }
    return render(request, 'app/todo_detail.html', context)

@login_required
def todo_detail_content(request, todo_id):
    """AJAX endpoint for todo detail content"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    notes = todo.notes.all()
    
    context = {
        'todo': todo,
        'notes': notes,
    }
    return render(request, 'app/todo_detail_content.html', context)

@login_required
def add_todo(request):
    """Add new todo"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            messages.success(request, 'Tarea creada exitosamente.')
            return redirect('dashboard')
    else:
        form = TodoForm()
    
    context = {
        'form': form,
        'categories': Category.objects.filter(user=request.user),
    }
    return render(request, 'app/add_todo.html', context)

@login_required
def add_todo_content(request):
    """AJAX endpoint for add todo form"""
    if request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return JsonResponse({'success': True, 'message': 'Tarea creada exitosamente.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = TodoForm()
    
    context = {
        'form': form,
        'categories': Category.objects.filter(user=request.user),
    }
    return render(request, 'app/add_todo_content.html', context)

@login_required
def edit_todo(request, todo_id):
    """Edit existing todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea actualizada exitosamente.')
            return redirect('todo_detail', todo_id=todo.id)
    else:
        form = TodoForm(instance=todo)
    
    context = {
        'form': form,
        'todo': todo,
        'categories': Category.objects.filter(user=request.user),
    }
    return render(request, 'app/edit_todo.html', context)

@login_required
def delete_todo(request, todo_id):
    """Delete todo"""
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('dashboard')
    return render(request, 'app/delete_todo.html', {'todo': todo})

@login_required
def categories(request):
    """Categories list view"""
    categories = Category.objects.filter(user=request.user)
    context = {
        'categories': categories,
    }
    return render(request, 'app/categories.html', context)

@login_required
def categories_content(request):
    """AJAX endpoint for categories content"""
    categories = Category.objects.filter(user=request.user)
    context = {
        'categories': categories,
    }
    return render(request, 'app/categories_content.html', context)

@login_required
def add_category(request):
    """Add new category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categories')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
    }
    return render(request, 'app/add_category.html', context)

@login_required
def edit_category(request, category_id):
    """Edit existing category"""
    category = get_object_or_404(Category, id=category_id, user=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'app/edit_category.html', context)

@login_required
def delete_category(request, category_id):
    """Delete category"""
    category = get_object_or_404(Category, id=category_id, user=request.user)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('categories')
    return render(request, 'app/delete_category.html', {'category': category})

@csrf_exempt
@login_required
def update_todo_status(request):
    """AJAX endpoint to update todo status (for drag & drop)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            todo_id = data.get('todo_id')
            new_status = data.get('status')
            new_order = data.get('order', 0)
            
            todo = get_object_or_404(Todo, id=todo_id, user=request.user)
            todo.status = new_status
            todo.order = new_order
            todo.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
