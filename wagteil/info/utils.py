from info.models import TablePage


def create_table_if_not_exist():
    table_page = TablePage.objects.first()

    if not table_page:
        ...
    else:
        ...
