from django.contrib import admin

from blog.models import Post, Category, Comment


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

@admin.register(Comment)
class CommentsManager(admin.ModelAdmin):
    autocomplete_fields = ('author',)
    list_display = ('author', 'post')
    raw_id_fields = ('post',)

