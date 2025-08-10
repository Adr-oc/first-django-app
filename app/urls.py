from django.urls import path
from . import views

urlpatterns = [
    # Dashboard and main views
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/content/', views.dashboard_content, name='dashboard_content'),
    
    # List view
    path('list/', views.list_view, name='list_view'),
    path('list/content/', views.list_view_content, name='list_view_content'),
    
    # Todo CRUD
    path('add/', views.add_todo, name='add_todo'),
    path('add/content/', views.add_todo_content, name='add_todo_content'),
    path('edit/<int:todo_id>/', views.edit_todo, name='edit_todo'),
    path('delete/<int:todo_id>/', views.delete_todo, name='delete_todo'),
    path('detail/<int:todo_id>/', views.todo_detail, name='todo_detail'),
    path('detail/<int:todo_id>/content/', views.todo_detail_content, name='todo_detail_content'),
    
    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/content/', views.categories_content, name='categories_content'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    
    # AJAX endpoints
    path('update-status/', views.update_todo_status, name='update_todo_status'),
]
