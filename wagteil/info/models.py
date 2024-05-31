from django.db.models import IntegerField, CharField
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock


class Tariff(Page):
    id_billing = IntegerField(verbose_name="ID биллинга")
    name = CharField(verbose_name="Имя тарифа", max_length=255)
    description = CharField(verbose_name="Описание тарифа", max_length=1024)

    content_panels = Page.content_panels + [
        FieldPanel('id_billing'),
        FieldPanel('name'),
        FieldPanel('description')
    ]

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class TableBlockCustom(TableBlock):
    ...


class TablePage(Page):
    table = StreamField([
        ('table', TableBlockCustom()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('table'),
    ]

    max_count = 1

    class Meta:
        verbose_name = 'Таблица по тарифам'
        verbose_name_plural = 'Таблица по тарифам'

