from django.shortcuts import redirect
from django.urls import reverse


class UserRoleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Код, вызываемый перед представлением при каждом запросе.
        if (request.path != '/cms/login/' and request.path != '/cms/logout/' and 'cms' in request.path
                and hasattr(request.user, 'role') and not request.user.role):
            return redirect(reverse('choose_role_admin'))
        response = self.get_response(request)
        # Код, вызываемый после представления при каждом запросе.
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Код, вызываемый непосредственно перед кодом представления.
        pass

    def process_exception(self, request, exception):
        # Код, вызываемый при выбросе исключения.
        pass

    def process_template_response(self, request, response):
        # Код, вызываемый при наличии в запросе метода render().
        return response
