from django.db.models import IntegerField, CharField
from django.shortcuts import render
from wagtail.fields import StreamField, StreamBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.utils.decorators import cached_classmethod
from wagtailcharts.blocks import ChartBlock
from wagtail.admin.panels import FieldPanel, ObjectList, TabbedInterface, PanelGroup
from wagtail.models import Page, PreviewableMixin
from users.choices import ROLE_USER


class Tariff(Page):
    id_billing = IntegerField(verbose_name="ID биллинга")
    name = CharField(verbose_name="Имя тарифа", max_length=255)
    description = CharField(verbose_name="Описание тарифа", max_length=1024)
    tariff_role = CharField(verbose_name="Для какой роли этот тариф",
                            max_length=255, null=True, blank=True, choices=ROLE_USER)

    content_panels = Page.content_panels + [
        FieldPanel('id_billing'),
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('tariff_role')
    ]

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'

    def serve(self, request, *args, **kwargs):
        return render(request, self.template, self.get_context(request))


class TableBlockCustom(TableBlock):
    ...


class TablePage(Page):
    template = 'table.html'

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


class ContentBlocks(StreamBlock):
    chart_block = ChartBlock()


class Chart(Page):

    template = 'chart.html'

    chart_data = StreamField([
        ('chart', ContentBlocks()),
    ], null=True, blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel('chart_data'),
    ]

    class Meta:
        verbose_name = 'График'
        verbose_name_plural = 'Графики'


class ObjectListCustomContent(PanelGroup):
    class BoundPanel(PanelGroup.BoundPanel):
        template_name = "wagtailadmin/custom_list.html"


class PivotTableTariff(Page, PreviewableMixin):
    edit_view_template_custom = "wagtailadmin/tariffs_shows.html"

    class Meta:
        verbose_name = "Сводная таблица по тарифам"
        verbose_name_plural = "Сводная таблица по тарифам"