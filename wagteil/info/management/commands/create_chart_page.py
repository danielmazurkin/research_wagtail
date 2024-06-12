from django.core.management.base import BaseCommand
from info.models import Chart, Page, ContentBlocks
from wagtail.fields import StreamField
from django.utils.text import slugify


class Command(BaseCommand):
    help = "Create a Chart page with custom data"

    def handle(self, *args, **options):
        # Define the parent page (e.g., Home page or any other existing page)
        home_page = Page.objects.get(slug='home')
        chart_page_id = None
        last_chart_page = Chart.objects.last()

        if not last_chart_page:
            chart_page_id = last_chart_page.id
        else:
            chart_page_id = 1

        # Instantiate the new Chart page
        chart_page = Chart(
            title=f"Chart page progammly {chart_page_id}",
            slug=slugify(f"Chart page progammly {chart_page_id}"),
        )

        # Define the StreamField value with custom chart data
        stream_value = StreamField([
            ('chart', (ContentBlocks()))
        ], use_json_field=True).to_python(
            [{'type': 'chart', 'value': [{'type': 'chart_block', 'value':
                {'chart_type': 'bar',
                'title': 'Страница для демонстрации работы графиков',
                'datasets':
                     '{"options":{"title":["","Второй столбец","Первый столбец","Третий столбец"],"color":["","#f47b27","#195c94","#195c94"],"yaxis":["","","",""]},"data":[["",""],["43","5"],["12","16"],["6","25"]]}',
                'settings': {'show_legend': True,
                             'html_legend': True,
                             'legend_position': 'top',
                             'reverse_legend': True,
                             'show_values_on_chart': True,
                             'precision': 1,
                             'show_grid': True,
                             'x_label': '',
                             'stacking': 'none',
                             'unit_override': '',
                             'y_left_min': '',
                             'y_left_max': '',
                             'y_left_step_size': '',
                             'y_left_label': '',
                             'y_left_data_type': 'number',
                             'y_left_precision': 0,
                             'y_left_show': True,
                             'y_right_min': '',
                             'y_right_max': '',
                             'y_right_step_size': '',
                             'y_right_label': '',
                             'y_right_data_type': 'number',
                             'y_right_precision': 0,
                             'y_right_show': True,
                             'pie_border_width': 2,
                             'pie_border_color': '#fff'}},
              'id': '7680f87f-6137-41d6-82cd-3aeccffebf69'}],
              'id': '9ef7d716-171a-4bbe-aac7-807b9ed68e9a'}]
        )
        chart_page.chart_data = stream_value
        home_page.add_child(instance=chart_page)
        # Save the page
        chart_page.save()

        # Publish the page if necessary
        chart_page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS('Successfully created a new Chart page with custom data'))
