from django.contrib import admin
from django.utils.html import format_html
from blog.models import Article, Category


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'thumbnail_tag', 'jpublish', 'is_special', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    raw_id_fields = ('author',)
    actions = ('make_published', 'make_draft')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-status', '-publish')

    @admin.action(description='انتشار مقالات انتخاب شده')
    def make_published(self, request, queryset):
        updated = queryset.update(status='p')
        self.message_user(request, f'{updated} مقاله منتشر شد.')

    @admin.action(description='پیش نویس شدن مقالات انتخاب شده')
    def make_draft(self, request, queryset):
        updated = queryset.update(status='d')
        self.message_user(request, f'{updated} مقاله پیش نویس شد.')

    @admin.display(description='تصویر مقاله')
    def thumbnail_tag(self, obj):
        return format_html('<img src="{}" width=100px height=75px style="border-radius: 5px;"/>'.format(obj.thumbnail.url))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'status', 'parent')
    list_filter = ('status',)
    actions = ('set_status_true', 'set_status_false')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}

    @admin.action(description='نمایش دادن دسته بندی های انتخاب شده')
    def set_status_true(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(request, f'{updated} دسته بندی قابل نمایش شد.')

    @admin.action(description='نمایش ندادن دسته بندی های انتخاب شده')
    def set_status_false(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(request, f'{updated} دسته بندی غیر قابل نمایش شد.')
