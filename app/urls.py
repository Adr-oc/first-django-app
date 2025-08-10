from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:category_id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:category_id>/delete/', views.delete_category, name='delete_category'),
    path('add/', views.add_todo, name='add_todo'),
    path('detail/<int:todo_id>/', views.todo_detail, name='todo_detail'),
    path('detail/<int:todo_id>/add-note/', views.add_note, name='add_note'),
    path('note/<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('toggle/<int:todo_id>/', views.toggle_todo, name='toggle_todo'),
    path('update-order/', views.update_todo_order, name='update_todo_order'),
]
