from django import forms
from users.choices import ROLE_USER


class UserRoleForm(forms.Form):

    role_select = forms.ChoiceField(choices=ROLE_USER)
