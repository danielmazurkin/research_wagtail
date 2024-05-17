from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel


class EntityInfo(models.Model):
    """Информация о сушности."""

    name = models.CharField(verbose_name="Имя темы",
                            max_length=255)

    text = models.TextField(verbose_name="Текст о теме")

    class Meta:
        verbose_name = "Текст"
        verbose_name_plural = "Тексты"


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]
