from django.contrib.contenttypes.fields import GenericRelation
from django.forms.utils import to_current_timezone
from comment.models import Comment
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
import jdatetime

User = get_user_model()

class IPAddress(models.Model):
    ip = models.GenericIPAddressField(unique=True, verbose_name='آدرس آیپی')

    class Meta:
        verbose_name = 'شناسه'
        verbose_name_plural = 'شناسه ها'

    def __str__(self):
        return self.ip


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name='children',
                               verbose_name='زیر گروه')
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
        ('d', 'پیش نویس'),  # draft
        ('p', 'منتشر شده'),  # publish
        ('i', 'در حال بررسی'),  # investigation
        ('b', 'برگشت داده شده'),  # back
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
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress, blank=True, through='ArticleHit', related_name='hits', verbose_name='بازدید ها')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('accounts:home')

    def jpublish(self):
        return jdatetime.datetime.fromgregorian(datetime=to_current_timezone(self.publish),locale='fa_IR').strftime('%a, %d %b %Y ساعت %H:%M')

    jpublish.short_description = 'زمان انتشار'

    def category_publish(self):
        return self.category.filter(status=True)

    def category_to_str(self):
        return ','.join([i.title for i in self.category_publish()])

    category_to_str.short_description = 'دسته بندی'


class ArticleHit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

