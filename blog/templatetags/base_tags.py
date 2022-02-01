from django import template
from ..models import Category

register = template.Library()


@register.inclusion_tag('partials/category_navbar.html')
def category_navbar():
    return {'category': Category.objects.filter(status=True)}


@register.simple_tag
def page_range(paginator, page_number):
    return paginator.get_elided_page_range(page_number, on_each_side=3, on_ends=2)


@register.inclusion_tag('registration/partials/link.html')
def link(request, link_name, content, classes):
    return {
        'request':request,
        'link_name':link_name,
        'classes': classes,
        'link':f'accounts:{link_name}',
        'content':content
    }