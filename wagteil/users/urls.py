from django.urls import path
from django.views.generic import TemplateView
from users.views import ChooseRoleView
from users.forms import UserRoleForm

urlpatterns = [
    path('choose/role',  TemplateView.as_view(template_name="choose_role.html",
                                              extra_context={"form": UserRoleForm()}), name='choose_role_admin'),
    path('choose', ChooseRoleView.as_view(), name='choose_role_select')
]

