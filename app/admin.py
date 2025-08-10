from django.contrib import admin
from .models import Todo, Category, Note

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'status', 'priority', 'completed', 'due_date', 'created_at')
    list_filter = ('status', 'priority', 'completed', 'category', 'created_at', 'user')
    search_fields = ('title', 'description', 'user__username', 'category__name')
    list_editable = ('status', 'priority', 'completed')
    date_hierarchy = 'created_at'
    ordering = ('todo_order', '-created_at')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('todo', 'content_preview', 'created_at')
    list_filter = ('created_at', 'todo__user')
    search_fields = ('content', 'todo__title')
    date_hierarchy = 'created_at'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Contenido'
