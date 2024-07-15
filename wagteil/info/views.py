from wagtail.admin.views.pages.listing import ExplorableIndexView
from wagtail.admin.views.pages import edit
from info.models import PivotTableTariff, Tariff


class InfoPageViewCustom(ExplorableIndexView):
    ...


class CustomPageEditCustom(edit.EditView):

    def get_template_names(self):
        if self.page.alias_of_id:
            return ["wagtailadmin/pages/edit_alias.html"]
        elif hasattr(self.page, 'edit_view_template_custom') and self.page.edit_view_template_custom is not None:
            return [self.page.edit_view_template_custom]
        else:
            return ["wagtailadmin/pages/edit.html"]

    def get(self, request):
        response = super().get(request)
        if isinstance(response.context_data['page'], PivotTableTariff):
            response.context_data['tariffs'] = Tariff.objects.all()
        return response
