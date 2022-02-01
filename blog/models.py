import jdatetime
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='زیر گروه')
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='پوزیشن')
    objects = CategoryManager()


    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ('parent__id', 'position',)

    def __str__(self):
        return self.title


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'), #draft
        ('p', 'منتشر شده'), #publish
        ('i', 'در حال بررسی'), #investigation
        ('b', 'برگشت داده شده'), #back
    )
    objects = ArticleManager()
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='articles', verbose_name='نویسنده')
    title = models.CharField(max_length=200, verbose_name='عنوان مقاله')
    category = models.ManyToManyField(Category, verbose_name='دسته بندی', related_name='articles')
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True, verbose_name='آدرس مقاله')
    description = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to='images', verbose_name='تصویر مقاله')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت')
    is_special = models.BooleanField(default=False, verbose_name='مقاله ویژه')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('accounts:home')

    def jpublish(self):
        return jdatetime.date.fromgregorian(date=self.publish.date()).strftime("%Y/%m/%d")

    jpublish.short_description = 'زمان انتشار'

    def category_publish(self):
        return self.category.filter(status=True)

    def category_to_str(self):
        return '/'.join([i.title for i in self.category_publish()])

    category_to_str.short_description = 'دسته بندی'
