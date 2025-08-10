from django.urls import path
from . import views

urlpatterns = [
    # Main views
    path('', views.dashboard, name='dashboard'),
    
    # Category management
    path('categories/', views.categories, name='categories'),
    path('category/add/', views.add_category, name='add_category'),
    path('category/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # Todo management
    path('add/', views.add_todo, name='add_todo'),
    path('detail/<int:todo_id>/', views.todo_detail, name='todo_detail'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    
    # Notes management
    path('note/add/<int:todo_id>/', views.add_note, name='add_note'),
    path('note/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    
    # AJAX endpoints
    path('update-order/', views.update_todo_order, name='update_todo_order'),
]
