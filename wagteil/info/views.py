from django.shortcuts import get_object_or_404
from wagtail.admin.views.pages.listing import ExplorableIndexView
from wagtail.models import Page
from django.conf import settings


class InfoPageViewCustom(ExplorableIndexView):
    ...
