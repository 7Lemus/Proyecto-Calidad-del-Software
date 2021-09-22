from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from tienda.models import Usuario


class UserForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email']
