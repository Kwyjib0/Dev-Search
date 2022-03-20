from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm # built in Django form, takes care of pw hashing
from django.contrib.auth.models import User # for authentication

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
            }
    # styles fields
    def __init__(self, *args, **kwargs):
        # override super
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # apply class 'input' to each field
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})