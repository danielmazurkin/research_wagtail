from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.images.api.v2.views import ImagesAPIViewSet
from wagtail.documents.api.v2.views import DocumentsAPIViewSet
# api.py
from wagtail.api.v2.router import WagtailAPIRouter
from wagtailmedia.api.views import MediaAPIViewSet


class MediaAPICustom(MediaAPIViewSet):
    # Require callers to be logged in, or provide the 'Authorization: Api-Key <key>' HTTP header with a valid key.
    permission_classes = []


# Создание маршрутизатора. "wagtailapi" это название URL.
api_router = WagtailAPIRouter('wagtailapi')

# # Этот параметр является классом endpoints, который обрабатывает запросы
api_router.register_endpoint('pages', PagesAPIViewSet)
api_router.register_endpoint('images', ImagesAPIViewSet)
api_router.register_endpoint('documents', DocumentsAPIViewSet)
api_router.register_endpoint("media", MediaAPICustom)
