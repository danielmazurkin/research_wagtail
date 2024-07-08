from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from wagtail.admin.views.account import LoginView
from users.models import CustomUser


class LoginViewCustom(LoginView):

    def form_valid(self, form):
        response = super().form_valid(form)

        if self.request.method == 'POST' and hasattr(self.request.user, 'role') and not self.request.user.role:
            return redirect(reverse('choose_role_admin'))

        return response


class ChooseRoleView(View):
    def post(self, request):
        if ('role_select' in request.POST and request.POST['role_select'] is not None
            and self.request.user is not None and hasattr(self.request.user, 'is_superuser')
            and self.request.user.is_superuser
        ):
            user = CustomUser.objects.filter(pk=request.user.pk).first()
            user.role = request.POST['role_select']
            user.save()
            return redirect(reverse('wagtailadmin_home'))
