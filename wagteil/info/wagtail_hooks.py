from wagtail import hooks
from info.models import Tariff


@hooks.register('construct_explorer_page_queryset')
def filter_pages_for_user(parent_page, pages, request):
    if isinstance(parent_page, Tariff):
        pages = pages.filter(tariff__tariff_role=request.user.role)
    return pages

