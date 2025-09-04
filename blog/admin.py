from django.contrib import admin

from blog.models import Post, Category


@admin.register(Post)
class PostManager(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ('users_liked',)


@admin.register(Category)
class CategoryManager(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}
