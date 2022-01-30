from django.apps import AppConfig
from django.core.paginator import Paginator
from django.utils.functional import cached_property
from sys import maxsize


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

