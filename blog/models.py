from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class Post(models.Model):
    title = models.CharField(unique=True, null=False)
    slug = models.SlugField(unique=True, allow_unicode=True, null=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(default=timezone.now)
    likes = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    users_liked = models.ManyToManyField(get_user_model(), blank=True, related_name='liked_posts')
    status = models.CharField(max_length=10, choices=(('draft', 'Draft'), ('published', 'Published')))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False, related_name='posts')
    featured_image = ProcessedImageField(
        upload_to='blog_images/%Y/%m/%d/',
        processors=[ResizeToFit(800, 800)],  # تغییر اندازه به حداکثر 800x800
        format='JPEG',  # ذخیره به فرمت JPEG برای امنیت و فشرده‌سازی
        options={'quality': 85},  # کیفیت 85 برای تعادل بین حجم و کیفیت
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.slug


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
