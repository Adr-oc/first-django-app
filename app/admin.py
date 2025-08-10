from django.contrib import admin
from .models import Todo, Category, Note

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'user__username']
    date_hierarchy = 'created_at'

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'category', 'user', 'created_at', 'due_date']
    list_filter = ['status', 'priority', 'category', 'created_at', 'due_date']
    search_fields = ['title', 'description', 'user__username']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'priority']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['todo', 'content_preview', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'todo__title']
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenido'
