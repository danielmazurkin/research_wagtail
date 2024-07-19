from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def edit_page_url(page):
    return reverse('wagtailadmin_pages:edit', args=[page.id])
