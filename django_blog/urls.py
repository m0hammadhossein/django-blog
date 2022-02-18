from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('comment/', include('comment.urls')),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('', include('blog.urls')),
    path('api/auth/', include('blog.api.urls')),
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)