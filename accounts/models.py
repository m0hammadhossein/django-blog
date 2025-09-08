from django.contrib.auth.models import AbstractUser
from django.db import models
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFit


class CustomUser(AbstractUser):
    avatar = ProcessedImageField(
        upload_to='blog_images/%Y/%m/%d/',
        processors=[ResizeToFit(800, 800)],  # تغییر اندازه به حداکثر 800x800
        format='JPEG',  # ذخیره به فرمت JPEG برای امنیت و فشرده‌سازی
        options={'quality': 85},  # کیفیت 85 برای تعادل بین حجم و کیفیت
        blank=True,
        null=True
    )
    biography = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
