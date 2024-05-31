from django.apps import AppConfig


class InfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'info'

    def ready(self):
        from wagtail.models import Page
        from info.models import TablePage, Tariff
        from wagtail.contrib.table_block.blocks import TableBlock
        from wagtail.fields import StreamField

        home_page = Page.objects.get(slug='home')
        table_page = TablePage.objects.first()

        if not table_page:
            tariffs = list(Tariff.objects.all().values_list('id_billing', 'name', 'description'))
            list_of_data_table = []
            list_of_data_table.append(['ID биллинга', 'Имя', 'Описание'])

            for tariff in tariffs:
                list_of_data_table.append(list(tariff))

            table_page = TablePage(
                title='Таблица по тарифам',
                slug="table-page",
            )
            table_data = {
                'data': list_of_data_table,
                'cell': [],
            }
            stream_value = StreamField([
                ('table', TableBlock())
            ], use_json_field=True).to_python([
                {'type': 'table', 'value': table_data}
            ])
            table_page.table = stream_value
            home_page.add_child(instance=table_page)
            table_page.save()