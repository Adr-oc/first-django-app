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
from .services import LocationIQService

# Landing page
def landing_page(request):
    return render(request, 'app/landing_page.html')

# Authentication views
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. ¡Ahora puedes iniciar sesión!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('landing_page')

# Main dashboard view
@login_required
def dashboard(request):
    todos = Todo.objects.filter(user=request.user).order_by('todo_order', '-created_at')
    categories = Category.objects.filter(user=request.user)
    
    # Group todos by status for Kanban view
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

# Category management
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
            Category.objects.create(
                name=name,
                color=color,
                user=request.user
            )
            messages.success(request, 'Categoría creada exitosamente.')
            
        return redirect('categories')
    
    return render(request, 'app/add_category.html')

@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    
    if request.method == 'POST':
        category.name = request.POST.get('name', category.name)
        category.color = request.POST.get('color', category.color)
        category.save()
        messages.success(request, 'Categoría actualizada exitosamente.')
        return redirect('categories')
    
    return render(request, 'app/edit_category.html', {'category': category})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, user=request.user)
    category.delete()
    messages.success(request, 'Categoría eliminada exitosamente.')
    return redirect('categories')

# Todo management
@login_required
def add_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        status = request.POST.get('status', 'todo')
        priority = request.POST.get('priority', 'medium')
        category_id = request.POST.get('category')
        
        if title:
            todo = Todo.objects.create(
                title=title,
                description=description,
                status=status,
                priority=priority,
                user=request.user
            )
            
            if category_id:
                try:
                    category = Category.objects.get(id=category_id, user=request.user)
                    todo.category = category
                    todo.save()
                except Category.DoesNotExist:
                    pass
                    
        return redirect('dashboard')
    
    categories = Category.objects.filter(user=request.user)
    return render(request, 'app/add_todo.html', {'categories': categories})

@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    categories = Category.objects.filter(user=request.user)
    
    if request.method == 'POST':
        # Update todo
        todo.title = request.POST.get('title', todo.title)
        todo.description = request.POST.get('description', todo.description)
        todo.status = request.POST.get('status', todo.status)
        todo.priority = request.POST.get('priority', todo.priority)
        todo.completed = request.POST.get('completed') == 'on'
        
        category_id = request.POST.get('category')
        if category_id:
            todo.category = Category.objects.get(id=category_id, user=request.user)
        else:
            todo.category = None
            
        due_date = request.POST.get('due_date')
        if due_date:
            from django.utils.dateparse import parse_datetime
            todo.due_date = parse_datetime(due_date)
        else:
            todo.due_date = None
            
        todo.save()
        messages.success(request, 'Tarea actualizada exitosamente.')
        return redirect('todo_detail', todo_id=todo.id)
    
    return render(request, 'app/todo_detail.html', {
        'todo': todo,
        'categories': categories
    })

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.delete()
    messages.success(request, 'Tarea eliminada exitosamente.')
    return redirect('dashboard')

@login_required
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect('dashboard')

# Notes management
@login_required
def add_note(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Note.objects.create(
                todo=todo,
                content=content
            )
            messages.success(request, 'Nota agregada exitosamente.')
            
    return redirect('todo_detail', todo_id=todo.id)

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, todo__user=request.user)
    todo_id = note.todo.id
    note.delete()
    messages.success(request, 'Nota eliminada exitosamente.')
    return redirect('todo_detail', todo_id=todo_id)

# AJAX endpoints
@csrf_exempt
@require_POST
@login_required
def update_todo_order(request):
    try:
        data = json.loads(request.body)
        todo_id = data.get('todo_id')
        new_status = data.get('status')
        new_order = data.get('order', 0)
        
        print(f"Updating todo {todo_id} to status {new_status} with order {new_order}")  # Debug
        
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        todo.status = new_status
        todo.todo_order = new_order
        todo.save()
        
        print(f"Todo updated successfully: {todo.title} -> {todo.status}")  # Debug
        
        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error updating todo: {str(e)}")  # Debug
        return JsonResponse({'success': False, 'error': str(e)})

# Location management
@csrf_exempt
@require_POST
@login_required
def update_todo_location(request, todo_id):
    """
    Vista AJAX para actualizar la ubicación de una tarea
    """
    try:
        todo = get_object_or_404(Todo, id=todo_id, user=request.user)
        data = json.loads(request.body)
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not latitude or not longitude:
            return JsonResponse({
                'success': False, 
                'error': 'Coordenadas requeridas'
            })
        
        # Validar que las coordenadas sean números válidos
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False, 
                'error': 'Coordenadas inválidas'
            })
        
        # Obtener dirección usando LocationIQ
        location_service = LocationIQService()
        
        if not location_service.is_api_key_valid():
            return JsonResponse({
                'success': False, 
                'error': 'API key de LocationIQ no configurada'
            })
        
        address_info = location_service.get_address_from_coordinates(latitude, longitude)
        
        if address_info:
            # Actualizar la tarea con la información de ubicación
            todo.latitude = latitude
            todo.longitude = longitude
            todo.address = address_info.get('formatted_address', '')
            todo.location_updated_at = timezone.now()
            todo.save()
            
            return JsonResponse({
                'success': True,
                'address': address_info.get('formatted_address', ''),
                'display_name': address_info.get('display_name', ''),
                'location_updated_at': todo.location_updated_at.isoformat()
            })
        else:
            return JsonResponse({
                'success': False, 
                'error': 'No se pudo obtener la dirección'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'error': f'Error interno: {str(e)}'
        })
